# -*- coding: utf-8 -*-  
import sys, os; _paths = filter(lambda _ : _.split('/')[-1] in ['src', 'HelloWord'], [os.path.realpath(__file__ + '/..' * (_ + 1)) for _ in range(os.path.realpath(__file__).count('/'))]); sys.path.extend([_[0] for _ in os.walk(_paths[0])] + [_[0] for _ in os.walk(_paths[1] + '/HelloWord-Lib/src')])
from util import *

class CircularCurler :

    def __init__(self) :
        self.clear()

    def clear(self) :
        self._flog        = sys.stdout
        self._num_working = 0
        self._timeout     = None
        self._is_quiet    = True
        self._tasks       = Queue()
        self._result_list = []
        self._trash_list  = []
        self._lock        = Lock()
        self.set_max_attempt(5) 
        return self

    def get_result_list(self) :
        return self._result_list

    def get_trash_list(self) :
        return self._trash_list

    def set_max_attempt(self, max_attempt) :
        self._max_attempt = max_attempt
        return self

    def set_timeout(self, timeout) :
        self._timeout = timeout
        return self

    def build_threads(self, num_worker_threads) :
        for i in range(num_worker_threads) :
            t = Thread(target = self._work)
            t.daemon = True
            t.start()
        return self

    def add_tasks(self, tasks) :
        _ = lambda task : task['config']
        for task in tasks :
            if task.get('log') is None    : task['log'] = _
            if task.get('result') is None : task['result'] = _
            if task.get('trash') is None  : task['trash'] = _
            self._tasks.put((0, task))
        return self

    def run(self, flog = sys.stdout, is_quiet = True) :
        self._flog = flog
        self._is_quiet = is_quiet
        self._tasks.join()
        return self

    def _log(self, flog, message) :
        flog.write('%s %s\n' % (ctime(), message))
        flog.flush()

    def _curl(self, task) :
        response = request(task['url'](task), timeout = self._timeout)
        if response['e'] is not None : return False
        try :
            content = response['content']
            result  = task['process'](content)
        except Exception, e :
            raise e
        return result

    def _work(self) :
        while True :
            self._lock.acquire()
            num_attempt, task = self._tasks.get()
            self._num_working += 1
            if num_attempt > 0 or not self._is_quiet :
                message = '%d %d %d %d %d %s' % (self._tasks.qsize(), self._num_working, len(self._result_list), len(self._trash_list), num_attempt, task['log'](task))
                self._log(sys.stdout, message)
                if self._flog != sys.stdout :
                    self._log(self._flog, message)
            self._lock.release()
            if num_attempt >= self._max_attempt :
                self._trash_list.append((num_attempt, task['trash'](task)))
            else :
                try :
                    result = self._curl(task)
                except KeyboardInterrupt, e :
                    self._tasks.task_done()
                    self._num_working -= 1
                    raise e
                except Exception, e :
                    self._trash_list.append((-1, task['trash'](task)))
                else :
                    if result is False :
                        self._tasks.put((num_attempt + 1, task))
                    else :
                        self._result_list.append((task['result'](task), result))
            self._tasks.task_done()
            self._num_working -= 1

if __name__ == '__main__':
    cc = CircularCurler()
