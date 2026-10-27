#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int
main(void)
{
  int pipefd[2];
  if (pipe(pipefd) < 0) {
    perror("pipe");
    return 1;
  }

  pid_t ls_pid = fork();
  if (ls_pid < 0) {
    perror("fork ls");
    return 1;
  }
  if (ls_pid == 0) {
    close(STDOUT_FILENO);
    if (dup(pipefd[1]) < 0) {
      perror("dup ls");
      exit(1);
    }
    close(pipefd[0]);
    close(pipefd[1]);
    execlp("ls", "ls", "/etc", (char *)NULL);
    perror("exec ls");
    exit(127);
  }

  pid_t wc_pid = fork();
  if (wc_pid < 0) {
    perror("fork wc");
    close(pipefd[0]);
    close(pipefd[1]);
    waitpid(ls_pid, NULL, 0);
    return 1;
  }
  if (wc_pid == 0) {
    close(STDIN_FILENO);
    if (dup(pipefd[0]) < 0) {
      perror("dup wc");
      exit(1);
    }
    close(pipefd[0]);
    close(pipefd[1]);
    execlp("wc", "wc", "-l", (char *)NULL);
    perror("exec wc");
    exit(127);
  }

  close(pipefd[0]);
  close(pipefd[1]);
  waitpid(ls_pid, NULL, 0);
  waitpid(wc_pid, NULL, 0);
  return 0;
}
