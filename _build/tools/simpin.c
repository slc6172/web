/* simpin.c — 以 simavr 執行 ATmega328P 韌體,記錄指定腳位的電位變化與 UART 輸出。
 * 用法: simpin firmware.elf SECONDS B0 [B1 D3 ...] [REG@88 ...] [IN@D2=0@500 ...](IN@腳位=電位@毫秒:模擬外部輸入,例如按鈕)
 * 舊說明:(REG@十六進位位址:每 10 ms 取樣一次暫存器)
 * 輸出: "PIN <名稱> <毫秒> <0|1>" 與 "UART <字元>" (逐行)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sim_avr.h"
#include "avr_ioport.h"
#include "avr_uart.h"
#include "avr_adc.h"
#include "sim_elf.h"

static avr_t *avr;
typedef struct { char name[8]; } pin_t;

static void pin_cb(struct avr_irq_t *irq, uint32_t value, void *param) {
    pin_t *p = (pin_t *)param;
    double ms = (double)avr->cycle * 1000.0 / (double)avr->frequency;
    printf("PIN %s %.3f %u\n", p->name, ms, value ? 1 : 0);
}
static void uart_cb(struct avr_irq_t *irq, uint32_t value, void *param) {
    printf("UART %u\n", value & 0xff);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: simpin fw.elf seconds PIN...\n"); return 2; }
    elf_firmware_t f; memset(&f, 0, sizeof f);
    if (elf_read_firmware(argv[1], &f)) { fprintf(stderr, "cannot read elf\n"); return 2; }
    strcpy(f.mmcu, "atmega328p"); f.frequency = 16000000;
    avr = avr_make_mcu_by_name("atmega328p");
    if (!avr) { fprintf(stderr, "no mcu\n"); return 2; }
    avr_init(avr);
    avr_load_firmware(avr, &f);
    avr->frequency = 16000000;
    double secs = atof(argv[2]);
    int nreg = 0; int regs[8];
    typedef struct { char port; int bit; int val; double ms; int done; } inev_t;
    inev_t ins[64]; int nin = 0;
    typedef struct { int byte; double ms; int done; } rx_t;
    rx_t rxs[64]; int nrx = 0;
    typedef struct { int ch; int mv; double ms; int done; } adc_t;
    adc_t adcs[64]; int nadc = 0;
    for (int i = 3; i < argc; i++) {
        if (strncmp(argv[i], "ADC@", 4) == 0) {   /* ADC@0=2500@500:在 500 ms 把 A0 的電壓設成 2500 mV */
            adc_t *a = &adcs[nadc++]; a->ch = atoi(argv[i] + 4);
            char *eq = strchr(argv[i], '='); char *at = strchr(eq, '@');
            a->mv = atoi(eq + 1); a->ms = atof(at + 1); a->done = 0;
            continue;
        }
        if (strncmp(argv[i], "RX@", 3) == 0) {   /* RX@500=49:在 500 ms 從序列埠送進一個位元組(49 = '1') */
            rx_t *r = &rxs[nrx++]; r->ms = atof(argv[i] + 3); r->byte = atoi(strchr(argv[i], '=') + 1); r->done = 0;
            continue;
        }
        if (strncmp(argv[i], "IN@", 3) == 0) {   /* IN@D2=0@500:在 500 ms 把 PD2 設成 0 */
            inev_t *e = &ins[nin++];
            e->port = argv[i][3]; e->bit = atoi(argv[i] + 4);
            char *eq = strchr(argv[i], '='); char *at = strchr(argv[i], '@'); at = strchr(at + 1, '@');
            e->val = atoi(eq + 1); e->ms = atof(at + 1); e->done = 0;
            continue;
        }
        if (strncmp(argv[i], "REG@", 4) == 0) { regs[nreg++] = (int)strtol(argv[i] + 4, NULL, 16); continue; }
        pin_t *p = malloc(sizeof *p); strncpy(p->name, argv[i], 7); p->name[7] = 0;
        char port = argv[i][0]; int bit = atoi(argv[i] + 1);
        avr_irq_t *irq = avr_io_getirq(avr, AVR_IOCTL_IOPORT_GETIRQ(port), bit);
        if (!irq) { fprintf(stderr, "bad pin %s\n", argv[i]); return 2; }
        avr_irq_register_notify(irq, pin_cb, p);
    }
    /* UART0 TX 輸出(Serial.print)*/
    avr_irq_t *u = avr_io_getirq(avr, AVR_IOCTL_UART_GETIRQ('0'), UART_IRQ_OUTPUT);
    if (u) avr_irq_register_notify(u, uart_cb, NULL);
    avr->vcc = avr->avcc = avr->aref = 5000;   /* 供電與參考電壓 5 V */
    /* 初始電位 */
    avr_cycle_count_t limit = (avr_cycle_count_t)(secs * 16000000.0);
    int state = cpu_Running;
    avr_cycle_count_t next = 0, step = 160000; /* 每 10 ms 取樣暫存器 */
    while (avr->cycle < limit && state != cpu_Done && state != cpu_Crashed) {
        state = avr_run(avr);
        if (nin) {
            double now = (double)avr->cycle * 1000.0 / 16000000.0;
            for (int q = 0; q < nin; q++)
                if (!ins[q].done && now >= ins[q].ms) {
                    ins[q].done = 1;
                    avr_raise_irq(avr_io_getirq(avr, AVR_IOCTL_IOPORT_GETIRQ(ins[q].port), ins[q].bit), ins[q].val);
                }
        }
        if (nadc) {
            double now = (double)avr->cycle * 1000.0 / 16000000.0;
            for (int q = 0; q < nadc; q++)
                if (!adcs[q].done && now >= adcs[q].ms) {
                    adcs[q].done = 1;
                    avr_raise_irq(avr_io_getirq(avr, AVR_IOCTL_ADC_GETIRQ, ADC_IRQ_ADC0 + adcs[q].ch), adcs[q].mv);
                }
        }
        if (nrx) {
            double now = (double)avr->cycle * 1000.0 / 16000000.0;
            for (int q = 0; q < nrx; q++)
                if (!rxs[q].done && now >= rxs[q].ms) {
                    rxs[q].done = 1;
                    avr_raise_irq(avr_io_getirq(avr, AVR_IOCTL_UART_GETIRQ('0'), UART_IRQ_INPUT), rxs[q].byte);
                }
        }
        if (nreg && avr->cycle >= next) {
            for (int r = 0; r < nreg; r++)
                printf("REG %x %.1f %u\n", regs[r], (double)avr->cycle * 1000.0 / 16000000.0, avr->data[regs[r]]);
            next += step;
        }
    }
    printf("END %.3f state=%d\n", (double)avr->cycle * 1000.0 / 16000000.0, state);
    return 0;
}
