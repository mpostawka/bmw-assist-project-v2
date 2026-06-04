#include <atomic>
#include <cstdint>
#include <fcntl.h>
#include <sys/mman.h>
#include <thread>
#include <unistd.h>

namespace {
const int row[3] = {16, 20, 21};
const int col[20] = {14, 4, 15, 17, 23, 27, 22, 24, 10, 9, 25, 11, 8, 7, 0, 5, 6, 13, 19, 26};
const int master = 12;

volatile uint32_t *gpio = nullptr;
uint8_t framebuffer[3][20];
std::atomic<bool> running{false};
std::thread worker;

void output(int pin) {
    int shift = (pin % 10) * 3;
    gpio[pin / 10] = (gpio[pin / 10] & ~(7u << shift)) | (1u << shift);
}
void high(int pin) { gpio[7] = 1u << pin; }
void low(int pin) { gpio[10] = 1u << pin; }

void refresh() {
    high(master);
    while (running) {
        for (int x = 0; x < 3; x++) {
            for (int y = 0; y < 20; y++)
                framebuffer[x][y] ? low(col[y]) : high(col[y]);
            high(row[x]);
            usleep(1250);
            low(row[x]);
        }
    }
    low(master);
}
}

extern "C" {

int screen_open() {
    int fd = open("/dev/gpiomem", O_RDWR | O_SYNC);
    if (fd < 0)
        return -1;
    gpio = (volatile uint32_t *)mmap(nullptr, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    close(fd);
    if (gpio == MAP_FAILED)
        return -1;
    for (int i = 0; i < 20; i++) {
        output(col[i]);
        high(col[i]);
    }
    for (int i = 0; i < 3; i++) {
        output(row[i]);
        low(row[i]);
    }
    output(master);
    low(master);
    running = true;
    worker = std::thread(refresh);
    return 0;
}

void screen_write(int x, int y, int value) { framebuffer[x][y] = (uint8_t)value; }

void screen_clear() {
    for (int x = 0; x < 3; x++)
        for (int y = 0; y < 20; y++)
            framebuffer[x][y] = 0;
}

void screen_close() {
    running = false;
    if (worker.joinable())
        worker.join();
}
}
