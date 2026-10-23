#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int
main(void)
{
  int first[2], second[2];
  if (pipe(first) < 0 || pipe(second) < 0) {
    perror("pipe");
    return 1;
  }

  pid_t producer = fork();
  if (producer < 0) {
    perror("fork ls");
    return 1;
  }
  if (producer == 0) {
    close(STDOUT_FILENO);
    if (dup(first[1]) < 0) { perror("dup ls"); exit(1); }
    close(first[0]); close(first[1]); close(second[0]); close(second[1]);
    execlp("ls", "ls", "/usr/bin", (char *)NULL);
    perror("exec ls");
    exit(127);
  }

  pid_t filter = fork();
  if (filter < 0) {
    perror("fork grep");
    return 1;
  }
  if (filter == 0) {
    close(STDIN_FILENO);
    if (dup(first[0]) < 0) { perror("dup grep input"); exit(1); }
    close(STDOUT_FILENO);
    if (dup(second[1]) < 0) { perror("dup grep output"); exit(1); }
    close(first[0]); close(first[1]); close(second[0]); close(second[1]);
    execlp("grep", "grep", "x", (char *)NULL);
    perror("exec grep");
    exit(127);
  }

  pid_t consumer = fork();
  if (consumer < 0) {
    perror("fork wc");
    return 1;
  }
  if (consumer == 0) {
    close(STDIN_FILENO);
    if (dup(second[0]) < 0) { perror("dup wc"); exit(1); }
    close(first[0]); close(first[1]); close(second[0]); close(second[1]);
    execlp("wc", "wc", "-l", (char *)NULL);
    perror("exec wc");
    exit(127);
  }

  close(first[0]); close(first[1]); close(second[0]); close(second[1]);
  waitpid(producer, NULL, 0);
  waitpid(filter, NULL, 0);
  waitpid(consumer, NULL, 0);
  return 0;
}
