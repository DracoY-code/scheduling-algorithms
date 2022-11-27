class Process:
    """The class to define a process.
    """
    def __init__(self, p_id: str, arrival_t: int, burst_t: int) -> None:
        self.p_id: str = p_id
        self.arrival_t: int = arrival_t
        self.burst_t: int = burst_t
        self.completion_t: int | None = None
        self.turnaround_t: int | None = None
        self.waiting_t: int | None = None

    def set_completion_t(self, completion_t: int) -> None:
        """Sets the process completion time.
        """
        if completion_t < self.burst_t:
            raise Exceptions.InvalidCompletionTimeError()
        self.completion_t = completion_t

    def set_turnaround_t(self) -> None:
        """Calculates and sets the process turnaround time.
        """
        if self.completion_t is None:
            return
        self.turnaround_t = self.completion_t - self.arrival_t

    def set_waiting_t(self) -> None:
        """Calculates and sets the process waiting time.
        """
        if self.turnaround_t is None:
            return
        self.waiting_t = self.turnaround_t - self.burst_t

    def print_process_data(self) -> None:
        """Prints the process details.
        """
        print(f'Process id      : {self.p_id}')
        print(f'Arrival time    : {self.arrival_t}')
        print(f'Burst time      : {self.burst_t}')
        print(f'Completion time : {self.completion_t}')
        print(f'Turnaround time : {self.turnaround_t}')
        print(f'Waiting time    : {self.waiting_t}\n')


class Scheduler:
    """The class to implement the FCFS scheduler.
    """
    def __init__(self) -> None:
        print('<<< First Come First Serve Scheduler >>>\n')
        self.running: Process | None = None
        self.ready_queue: list[Process] = []
        self.history: list[Process] = []
        self.total_t: int = 0

    def add_process(self, p: Process) -> None:
        """Adds a process to the scheduler.
        """
        if self.running is None:
            self.running = p
        else:
            self.ready_queue.append(p)

    def execute(self) -> None:
        """Executes the scheduler.
        """
        while self.running:
            self.update_running_process()
            self.history.append(self.running)
            try:
                self.running = self.ready_queue.pop(0)
            except IndexError:
                self.running = None

    def update_running_process(self) -> None:
        """Updates the fields of the running process.
        """
        if self.running is None:
            return
        self.total_t += self.running.burst_t
        self.running.set_completion_t(self.total_t)
        self.running.set_turnaround_t()
        self.running.set_waiting_t()

    def calc_avg_turnaround_t(self) -> float:
        """Calculates and returns the average turnaround time of the scheduler.
        """
        total_turnaround_t: int = 0
        for p in self.history:
            if p.turnaround_t is None:
                raise Exceptions.MissingTurnaroundTimeError(p)
            total_turnaround_t += p.turnaround_t
        return total_turnaround_t / len(self.history)
    
    def calc_avg_waiting_t(self) -> float:
        """Calculates and returns the average waiting time of the scheduler.
        """
        total_waiting_t: int = 0
        for p in self.history:
            if p.waiting_t is None:
                raise Exceptions.MissingWaitingTimeError(p)
            total_waiting_t += p.waiting_t
        return total_waiting_t / len(self.history)

    def print_gantt_chart(self) -> None:
        """Prints the Gantt chart for the scheduled processes.
        """
        print('Gantt chart: ', end='')
        for p in self.history:
            for _ in range(int(p.burst_t)):
                print(f'|{p.p_id}', end='')
        print('|\n')

    def print_history(self) -> None:
        """Prints the scheduler history.
        """
        headers: list[str] = ['PID',
                              'Arrival Time',
                              'Burst Time',
                              'Completion Time',
                              'Turnaround Time',
                              'Waiting Time']
        paddings: list[int] = [len(header) for header in headers]
        separator: str = '-' * (sum(paddings) + 3 * len(paddings) - 1)

        for i in range(len(headers)):
            print(f' {headers[i].ljust(paddings[i])} ', end='')
            if i == len(headers) - 1:
                print()
            else:
                print('|', end='')                
        print(separator)

        for p in self.history:
            details: list[str | int | None] = list(vars(p).values())
            for k in range(len(paddings)):
                print(f' {details[k]:{paddings[k]}} ', end='')
                if k == len(paddings) - 1:
                    print()
                else:
                    print('', end='|')
        print(separator, end='\n\n')


class Exceptions:
    """The exception class for the module.
    """
    class InvalidCompletionTimeError(BaseException):
        """The class to implement a completion time exception.
        """
        error_txt: str = 'completion time is smaller than the burst time'
        def __init__(self, e: str=error_txt) -> None:
            super().__init__(e)

    class MissingTurnaroundTimeError(BaseException):
        """The class to implement a turnaround time exception.
        """
        error_txt: str = 'turnaround time is missing'
        def __init__(self, p: Process, e: str=error_txt) -> None:
            super().__init__(f'{e} for {p.p_id}')

    class MissingWaitingTimeError(BaseException):
        """The class to implement a waiting time exception.
        """
        error_txt: str = 'waiting time is missing'
        def __init__(self, p: Process, e: str=error_txt) -> None:
            super().__init__(f'{e} for {p.p_id}')


if __name__ == '__main__':
    scheduler: Scheduler = Scheduler()
    processes: list[Process]

    p0: Process = Process('P0', 0, 5)
    p1: Process = Process('P1', 1, 3)
    p2: Process = Process('P2', 2, 8)
    p3: Process = Process('P3', 3, 6)

    processes = [p0, p1, p2, p3]
    for p in processes:
        scheduler.add_process(p)
    scheduler.execute()
    
    scheduler.print_history()
    scheduler.print_gantt_chart()
    print(f'Average turnaround time : {scheduler.calc_avg_turnaround_t()}')
    print(f'Average waiting time    : {scheduler.calc_avg_waiting_t()}')
