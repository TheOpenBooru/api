from openbooru.modules.daemon.task import Task
import pytest
import time


def test_Task_Runs_Async_Function():
    var = []
    # Mutable variables transcends threads
    async def thread_target():
        var.append(True)
    
    task = Task(id="Test Async", function=thread_target)
    task.start()
    
    time.sleep(0.01)
    assert task.isAsync == True, "Didn't detect sync function"
    assert var == [True], "Task didn't run"


def test_Task_Runs_Sync_Function():
    var = []
    # Mutable variables transcends threads
    def thread_target():
        var.append(True)
    
    task = Task(id="Test Sync", function=thread_target)
    task.start()
    
    time.sleep(0.01)
    assert task.isAsync == False, "Didn't detect sync function"
    assert var == [True], "Task didn't run"


@pytest.mark.skip("TODO")
def test_Task_Running_Updated_Correctly():
    def thread_target():
        time.sleep(0.05)
    
    task = Task(id="Test Running", function=thread_target)
    task.start()
    
    time.sleep(0.01)
    assert task.running == True, ""
    time.sleep(0.1)
    assert task.running == False, ""


@pytest.mark.skip("TODO")
def test_Task_Stop_Works():
    def thread_target():
        time.sleep(0.5)
    
    task = Task(id="Test Stop", function=thread_target)
    
    task.start()
    start = time.time()
    task.stop()
    end = time.time()

    duration = (end - start)
    assert duration < 0.5, "Didn't stop execution correctly"
    assert task.running == False, "Stop didn't update running state"


@pytest.mark.skip("TODO")
def test_Task_Retry_After_Works():
    var = []
    def thread_target():
        var.append(True)
    
    task = Task(id="Test Stop", function=thread_target, retry_after=0.01)
    
    task.start()
    time.sleep(0.01)
    assert var == [True], "Didn't Run the First Time"
    time.sleep(0.11)
    assert var == [True,True], "Didn't Re-run the Function"
    task.stop()

