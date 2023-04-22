#include <linux/sched.h>
#include <net/sock.h>
#include <net/inet_sock.h>
#include <linux/tcp.h>
#include <linux/mptcp.h>

struct ipv4_conn_info_t {
    u32 pid;
    u32 saddr;
    u32 daddr;
    u16 sport;
    u16 dport;
};

BPF_HASH(start, u32, u64);
BPF_PERF_OUTPUT(ipv4_events);

int kprobe__tcp_v4_connect(struct pt_regs *ctx, struct sock *sk) {
    u64 start_ns = bpf_ktime_get_ns();
    u32 pid = bpf_get_current_pid_tgid();

    start.update(&pid, &start_ns);

    return 0;
}

int kretprobe__tcp_v4_connect(struct pt_regs *ctx) {
    int ret = PT_REGS_RC(ctx);
    if (ret != 0)
        return 0;

    u32 pid = bpf_get_current_pid_tgid();
    u64 *start_ns = start.lookup(&pid);
    if (!start_ns)
        return 0;

    u64 delta_ns = bpf_ktime_get_ns() - *start_ns;

    struct sock *sk = (struct sock *)PT_REGS_PARM1(ctx);
    if (!sk)
        return 0;

    struct inet_sock *inet = inet_sk(sk);
    if (!inet)
        return 0;

    if (!sk->sk_socket || !sk->sk_socket->file || !sk->sk_socket->file->f_inode)
        return 0;

    struct tcp_sock *tp = tcp_sk(sk);
    if (!tp)
        return 0;

    struct ipv4_conn_info_t info = {};
    info.pid = pid;
    info.saddr = inet->inet_saddr;
    info.daddr = inet->inet_daddr;
    info.sport = bpf_ntohs(inet->inet_sport);
    info.dport = bpf_ntohs(inet->inet_dport);

    ipv4_events.perf_submit(ctx, &info, sizeof(info));

    return 0;
}
