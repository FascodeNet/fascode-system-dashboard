[CCode(cheader_filename = "glibtop.h", lower_case_cprefix = "glibtop_")]
namespace GTop {
    public void init();

    [CCode(cname = "glibtop_cpu", cheader_filename = "glibtop/cpu.h")]
    public struct Cpu {
        uint64 flags;
        uint64 total;
        uint64 user;
        uint64 nice;
        uint64 sys;
        uint64 idle;
        uint64 iowait;
        uint64 irq;
        uint64 softirq;
        uint64 frequency;
        uint64 xcpu_total[1024];
        uint64 xcpu_user[1024];
        uint64 xcpu_nice[1024];
        uint64 xcpu_sys[1024];
        uint64 xcpu_idle[1024];
        uint64 xcpu_iowait[1024];
        uint64 xcpu_irq[1024];
        uint64 xcpu_softirq[1024];
        uint64 xcpu_flags;
    }
    public void get_cpu(out Cpu cpu);

    [CCode(cname = "glibtop_mem", cheader_filename = "glibtop/mem.h")]
    public struct Mem {
        uint64 flags;
        uint64 total;
        uint64 used;
        uint64 free;
        uint64 shared;
        uint64 buffer;
        uint64 cached;
        uint64 user;
        uint64 locked;
    }
    public void get_mem(out Mem mem);

    [CCode(cname = "glibtop_swap", cheader_filename = "glibtop/swap.h")]
    public struct Swap {
        uint64 flags;
        uint64 total;
        uint64 used;
        uint64 free;
        uint64 pagein;
        uint64 pageout;
    }
    public void get_swap(out Swap swap);

    [CCode(cname = "glibtop_fsusage", cheader_filename = "glibtop/fsusage.h")]
    public struct FsUsage {
        uint64 flags;
        uint64 blocks;
        uint64 bfree;
        uint64 bavail;
        uint64 files;
        uint64 ffree;
        uint32 block_size;
        uint64 read;
        uint64 write;
    }

    public void get_fsusage(out FsUsage fsusage, string mount_dir);

    [CCode(cname = "glibtop_netload", cheader_filename = "glibtop/netload.h")]
    public struct NetLoad {
        uint64 flags;
        uint64 if_flags;
        uint32 mtu;
        uint32 subnet;
        uint32 address;
        uint64 packets_in;
        uint64 packets_out;
        uint64 packets_total;
        uint64 bytes_in;
        uint64 bytes_out;
        uint64 bytes_total;
        uint64 errors_in;
        uint64 errors_out;
        uint64 errors_total;
        uint64 collisions;
        uint8 address6[16];
        uint8 prefix6[16];
        uint8 scope6;
        uint8 hwaddress[8];
    }

    public void get_netload(out NetLoad netload, string device);

    [CCode(cname = "glibtop_netlist", cheader_filename = "glibtop/netlist.h")]
    public struct NetList {
        uint64 flags;
        uint32 number;
    }

    [CCode(array_length = false, array_null_terminated = true)]
    public string[] get_netlist(out NetList netlist);
}
