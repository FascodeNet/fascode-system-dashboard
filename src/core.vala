namespace Dashboard {
    public class Core: Object {
        private Core core;
        private uint64 cpu_old_total;
        private uint64 cpu_old_used;
        public  double cpu_percentage = 0;
        public double mem_percentage = 0;
        public bool is_swap = false;
        public double swap_percentage = 0;
        private uint64 disk_old_read;
        private uint64 disk_old_write;
        public uint64 disk_read = 0;
        public uint64 disk_write = 0;
        public uint64 net_send = 0;
        public uint64 net_recive = 0;

        public Core get_default() {
            if (core == null) {
                core = new Core();
            }
        }

        public Core {
            GTop.Cpu cpu;
            GTop.get_cpu(out cpu);

            uint64 used = cpu.user + cpu.nice + cpu.sys;
            cpu_old_total = cpu.total;
            cpu_old_used = used;

            GTop.Swap swap;
            GTop.get_swap(out swap);

            if (swap.total != 0) {
                is_swap = true;
            }

            GTop.FsUsage fsusage;
            GTop.get_fsusage(out fsusage, "/");;

            disk_old_read = fsusage.read;
            disk_old_write = fsusage.write;

            Timeout.add(100, this.update);
        }

        public bool update() {
            GTop.Cpu cpu;
            GTop.get_cpu(out cpu);

            uint64 used = cpu.user + cpu.nice + cpu.sys;
            cpu_percentage = (((double) (used - old_used)) / (cpu.total - old_total)) * 100;
            cpu_old_total = cpu.total;
            cpu_old_used = used;

            GTop.Mem mem;
            GTop.get_mem(out mem);

            mem_percentage = (((double) mem.user / mem.total) * 100);

            if (is_swap) {
                GTop.Swap swap;
                GTop.get_swap(out swap);

                swap_percentage = (((double) swap.used / swap.total) * 100);
            }

            GTop.FsUsage fsusage;
            GTop.get_fsusage(out fsusage, "/");;

            disk_read = (fsusage.read - old_read) * 10;
            disk_write = (fsusage.write - old_write) * 10;
            disk_old_read = fsusage.read;
            disk_old_write = fsusage.write;

            return true;
        }
    }
}