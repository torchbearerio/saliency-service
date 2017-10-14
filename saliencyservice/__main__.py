import SalNet
from pythoncore import Constants, WorkerService


def handle_task(task_input, task_token):
    ep_id = task_input["epId"]
    hit_id = task_input["hitId"]
    print("Received saliency task for ep {}, hit {}".format(ep_id, hit_id))
    sn = SalNet.SalNet(ep_id, hit_id, task_token)
    sn.run()

if __name__ == '__main__':
    print("Welcome to Saliency Service")
    # handle_task({"epId": 437, "hitId": 123}, "asdf")
    thisTask = Constants.TASK_ARNS['CV_SALIENCY']

    WorkerService.start((thisTask, handle_task))



