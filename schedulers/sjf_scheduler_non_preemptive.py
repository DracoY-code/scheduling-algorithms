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
    """The class to implement the SJF scheduler.
    """
    def __init__(self) -> None:
        print('<<< Shortest Job First Scheduler: Non-Preemptive >>>\n')
        self.running: Process | None = None
        self.ready_queue: list[Process] = []
        self.history: list[Process] = []
        self.total_t: int = 0

    def add_process(self, p: Process) -> None:
        """Adds a process to the scheduler.
        """
        self.ready_queue.append(p)

    def setup(self) -> None:
        """Sorts the ready queue and assigns the initial running process.
        """
        self.ready_queue.sort(key=lambda p: p.arrival_t)
        self.running = self.ready_queue.pop(0)
        
    def execute(self) -> None:
        """Executes the scheduler.
        """
        self.setup()
        while self.running:
            self.update_running_process()
            self.history.append(self.running)

            # Manipulate the ready queue on the basis
            # of shortest burst time here
            self.set_highest_priority_process()

    def update_running_process(self) -> None:
        """Updates the fields of the running process.
        """
        if self.running is None:
            return
        self.total_t += self.running.burst_t
        self.running.set_completion_t(self.total_t)
        self.running.set_turnaround_t()
        self.running.set_waiting_t()

    def set_highest_priority_process(self) -> None:
        """Compares processes in the ready queue and sets the process with
        smallest burst time as the running process.
        """
        try:
            self.running = min(filter(
                lambda p: p.arrival_t <= self.total_t,
                self.ready_queue
            ), key=lambda p: p.burst_t)
            self.ready_queue.remove(self.running)
        except ValueError:
            self.running = None

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

    p1: Process = Process('P1', 2, 6)
    p2: Process = Process('P2', 5, 2)
    p3: Process = Process('P3', 1, 8)
    p4: Process = Process('P4', 0, 3)
    p5: Process = Process('P5', 4, 4)

    processes = [p1, p2, p3, p4, p5]
    for p in processes:
        scheduler.add_process(p)
    scheduler.execute()

    scheduler.print_history()
    scheduler.print_gantt_chart()
    print(f'Average turnaround time : {scheduler.calc_avg_turnaround_t()}')
    print(f'Average waiting time    : {scheduler.calc_avg_waiting_t()}')
