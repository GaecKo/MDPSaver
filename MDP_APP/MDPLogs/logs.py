import time as t

class Log:
    def __init__(self):
        self.log_file = "MDPLogs/log_file/logs.txt"
    
    def two_numbers(self, number):
        if len(str(number)) < 2:
            return F"0{str(number)}"
        return str(number)

    def create_log(self, action) -> str:
        current = list(t.localtime())
        year, month, day,  = current[0], self.two_numbers(current[1]), self.two_numbers(current[2])
        hour, min, sec = self.two_numbers(current[3]), self.two_numbers(current[4]), self.two_numbers(current[5])
        
        with open(self.log_file, 'a') as file:
            file.write(F"[{day}/{month}/{year} | {hour}:{min} ({sec})] {action.upper()} \n" )     