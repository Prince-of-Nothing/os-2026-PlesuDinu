#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int
main(void)
{
  printf("parent: my PID is %d\n", getpid());
  fflush(stdout);

  pid_t pid = fork();
  if (pid < 0) {
    perror("fork");
    return 1;
  }

  if (pid == 0) {
    printf("child: my PID is %d, my parent is %d\n", getpid(), getppid());
    fflush(stdout);
    execlp("ls", "ls", "-l", (char *)NULL);
    perror("exec");
    exit(127);
  }

  int status;
  sleep(20);
  if (waitpid(pid, &status, 0) < 0) {
    perror("waitpid");
    return 1;
  }
  printf("parent: child %d was reaped\n", pid);
  return 0;
}
