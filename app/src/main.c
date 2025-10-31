#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

/* CPU load */
#include <zephyr/debug/cpu_load.h>      /* cpu_load_get() */

/* Heap (RAM) stats */
#include <zephyr/sys/sys_heap.h>
#include <zephyr/sys/mem_stats.h>
extern struct sys_heap _system_heap;    /* system heap backing k_malloc() */

/* Power management notifier (older API: state_entry/state_exit only) */
#include <zephyr/pm/pm.h>

#include <buildCfg.h>
#include <inputCfg.h>


static int64_t  sleep_enter_ms = -1;
static uint64_t total_sleep_ms = 0;
static uint64_t sleep_per_reporting_cycle_ms = 0;

static void pm_state_entry_cb(enum pm_state state)
{
    printk("PM: Entering power state %d\n", state);
    // Track all power states, including SUSPEND_TO_IDLE
    sleep_enter_ms = k_uptime_get();
}

static void pm_state_exit_cb(enum pm_state state)
{
    printk("PM: Exiting power state %d\n", state);
    // Track sleep time for all power states
    if (sleep_enter_ms >= 0) {
        int64_t dt = k_uptime_get() - sleep_enter_ms;
        if (dt > 0) {
            total_sleep_ms += (uint64_t)dt;
            sleep_per_reporting_cycle_ms += (uint64_t)dt;
        }
        sleep_enter_ms = -1;
    }
}

/* Correct notifier for this API */
static struct pm_notifier pm_nb = {
    .state_entry = pm_state_entry_cb,
    .state_exit  = pm_state_exit_cb,
};

void main(void)
{
#if IS_ENABLED(CONFIG_PM)
    pm_notifier_register(&pm_nb);
#endif

    const uint32_t report_period_ms = 5000;
    uint64_t last_print_ms = k_uptime_get();
    uint32_t counter = 0;

    while (1) {

        uint64_t now = k_uptime_get();
        //report system performance every report_period_ms
        if ((now - last_print_ms) >= report_period_ms) {
            /* CPU load: per-mille -> percent */
            int load_pm  = cpu_load_get(true);   /* reset measurement window */
            int load_pct = (load_pm >= 0) ? (load_pm / 10) : -1;

            uint64_t up_ms   = now;
            uint64_t run_ms  = up_ms - total_sleep_ms;

            if (load_pct >= 0) {
                printk("CPU=%d%% | Uptime=%llu ms (Run=%llu, Sleep=%llu, SleepPerCycle=%llu)\n",
                       load_pct,
                       up_ms, run_ms, total_sleep_ms, sleep_per_reporting_cycle_ms);
            } else {
                printk("CPU=%s | Uptime=%llu ms (Run=%llu, Sleep=%llu, SleepPerCycle=%llu) \n",
                       (load_pct >= 0) ? "n/a" : "n/a",
                       up_ms, run_ms, total_sleep_ms, sleep_per_reporting_cycle_ms);
            }
            sleep_per_reporting_cycle_ms = 0;
            last_print_ms = now;
        }

        //go to sleep deep sleep based on input config
        if (counter < SLEEP_CYCLE) {
            printk("Start of short sleep\n");
            k_sleep(K_MSEC(100));
        }else{
            printk("Start of long sleep\n");
            counter = 0;
            k_sleep(K_MSEC(1000));
        }
        counter++;
    }
}

/* Custom Power Management Policy - Makes your settings the default */
#if IS_ENABLED(CONFIG_PM_POLICY_CUSTOM)

const struct pm_state_info *pm_policy_next_state(uint8_t cpu, int32_t ticks)
{
    /* Default power state configuration - your desired settings */
    static const struct pm_state_info default_suspend_to_idle = {
        .state = PM_STATE_SUSPEND_TO_IDLE,
        .substate_id = 0,
        .min_residency_us = 500,    /* Must sleep at least 500us to be worthwhile */
        .exit_latency_us = 100       /* Takes 100μs to wake up */
    };

    /* Convert ticks to microseconds for comparison */
    uint32_t idle_us = k_ticks_to_us_ceil32(ticks);
    
    /* Only enter power state if idle time is sufficient */
    if (idle_us >= default_suspend_to_idle.min_residency_us) {
        printk("PM Policy: Entering SUSPEND_TO_IDLE (idle=%u us)\n", idle_us);
        return &default_suspend_to_idle;
    }
    return NULL;
}

#endif /* CONFIG_PM_POLICY_CUSTOM */
