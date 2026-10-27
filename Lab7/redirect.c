#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>

int
main(void)
{
  pid_t pid = fork();
  if (pid < 0) {
    perror("fork");
    return 1;
  }
  if (pid == 0) {
    close(STDOUT_FILENO);
    int fd = open("out.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
      perror("open");
      exit(1);
    }
    fprintf(stderr, "open gave descriptor %d\n", fd);
    execlp("ls", "ls", "-l", (char *)NULL);
    perror("exec");
    exit(127);
  }

  if (waitpid(pid, NULL, 0) < 0) {
    perror("waitpid");
    return 1;
  }
  printf("done: the listing is in out.txt\n");
  return 0;
}
