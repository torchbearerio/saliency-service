import Algorithmia
from Algorithmia.algo_response import AlgoException
from pythoncore import Vault, Task, Constants
from pythoncore.AWS import AWSClient

# Build Algorithmia client
key = Vault.get_key('algorithmia-key')
client = Algorithmia.client(key)


class SalNet (Task.Task):

    def __init__(self, ep_id, hit_id, task_token):
        super(SalNet, self).__init__(ep_id, hit_id, task_token)

    def __run_salnet(self):
        # Loop through all positions
        bucket = Constants.S3_BUCKETS['STREETVIEW_IMAGES']
        for position in Constants.LANDMARK_POSITIONS.values():
            print("Running SalNet for position {} of hit {}".format(position, self.hit_id))
            # See if we have an image for this position; run SalNet if so
            if AWSClient.s3_key_exists(bucket, "{}_{}.jpg".format(self.ep_id, position)):
                # Pass in file and pass in args required from the algorithm FpGrowth
                params = {
                    "image": 's3+S3://torchbearer-sv-images/{}_{}.jpg'.format(self.ep_id, position),
                    "saliencyLocation": 's3+S3://torchbearer-saliency-maps/{}_{}.json'.format(self.hit_id, position),
                }

                algo = client.algo('deeplearning/SalNet/0.2.0')

                # Run SalNet, then return
                response = None
                try:
                    response = algo.pipe(params)

                except AlgoException:
                    self.send_failure('SALNET_ERROR', response.error.message)

        self.send_success()
        print("Completed saliency task for ep {}, hit {}".format(self.ep_id, self.hit_id))

    def run(self):
        self.__run_salnet()

if __name__ == '__main__':
    sn = SalNet(437, 12, "sdfasdf")
    sn.run()
