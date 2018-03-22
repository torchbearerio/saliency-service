import Algorithmia
from Algorithmia.algo_response import AlgoException
from pythoncore import Vault, Task, Constants
from pythoncore.AWS import AWSClient
from pythoncore.Model.Hit import Hit
from pythoncore.Model import TorchbearerDB
import time

# Build Algorithmia client
key = Vault.get_key('algorithmia-key')
client = Algorithmia.client(key)


class SalNet (Task.Task):

    def __init__(self, ep_id, hit_id, task_token):
        super(SalNet, self).__init__(ep_id, hit_id, task_token)

    def __run_salnet(self):
        session = TorchbearerDB.Session()
        hit = session.query(Hit).filter_by(hit_id=self.hit_id).one()
        hit.set_start_time_for_task("cv_saliency")

        # Loop through all positions
        bucket = Constants.S3_BUCKETS['STREETVIEW_IMAGES']
        for position in Constants.LANDMARK_POSITIONS.values():
            print("Running SalNet for position {} of hit {}".format(position, self.hit_id))
            # See if we have an image for this position; run SalNet if so
            if AWSClient.s3_key_exists(bucket, "{}_{}.jpg".format(self.hit_id, position)):
                # Pass in file and pass in args required from the algorithm FpGrowth
                params = {
                    "image": 's3+SVImages://torchbearer-sv-images/{}_{}.jpg'.format(self.hit_id, position),
                    "saliencyLocation": 's3+SVImages://torchbearer-saliency-maps/{}_{}.json'.format(self.hit_id, position),
                }

                algo = client.algo('deeplearning/SalNet/0.2.0')

                # Run SalNet, then return
                try:
                    algo.pipe(params)

                except AlgoException as error:
                    self.send_failure('SALNET_ERROR', error.message)

        self.send_success()
        hit.set_end_time_for_task("cv_saliency")
        session.commit()
        session.close()

        print("Completed saliency task for ep {}, hit {}".format(self.ep_id, self.hit_id))

    def run(self):
        self.__run_salnet()

if __name__ == '__main__':
    sn = SalNet(437, 12, "sdfasdf")
    sn.run()
