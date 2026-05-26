#include <svo/config.h>
#include <svo/frame_handler_mono.h>
#include <svo/map.h>
#include <svo/frame.h>
#include <vector>
#include <string>
#include <vikit/math_utils.h>
#include <vikit/vision.h>
#include <vikit/abstract_camera.h>
#include <vikit/atan_camera.h>
#include <vikit/pinhole_camera.h>
#include <opencv2/opencv.hpp>
#include <sophus/se3.h>
#include <iostream>

namespace svo {

class BenchmarkNodeKITTI
{
  vk::AbstractCamera* cam_;
  svo::FrameHandlerMono* vo_;

public:
  BenchmarkNodeKITTI();
  ~BenchmarkNodeKITTI();
  void runFromFolder(const std::string &dataset_dir, const std::string &pattern,
                     int start_idx, int end_idx);
};

BenchmarkNodeKITTI::BenchmarkNodeKITTI()
  : cam_(NULL), vo_(NULL)
{}

BenchmarkNodeKITTI::~BenchmarkNodeKITTI()
{
  delete vo_;
  delete cam_;
}

void BenchmarkNodeKITTI::runFromFolder(const std::string &dataset_dir, const std::string &pattern,
                                       int start_idx, int end_idx)
{
  const int BUFFER = 1024;
  char filename[BUFFER];
  bool pattern_is_valid = true;
  bool first = true;

  for(int img_id = start_idx; img_id <= end_idx; ++img_id)
  {
    snprintf(filename, BUFFER, (dataset_dir + "/" + pattern).c_str(), img_id);
    if(first) {
      cv::Mat img(cv::imread(filename, 0));
      if(img.empty()) {
        std::cerr << "Failed to open first image '" << filename << "'\n";
        return;
      }

      // create camera with KITTI defaults if image size matches KITTI, else use center principal point
      if(img.cols == 1241 && img.rows == 376)
        cam_ = new vk::PinholeCamera(1241, 376, 718.8560, 718.8560, 607.1928, 185.2157);
      else
        cam_ = new vk::PinholeCamera(img.cols, img.rows, 718.8560, 718.8560, img.cols/2.0, img.rows/2.0);

      vo_ = new svo::FrameHandlerMono(cam_);
      vo_->start();

      double timestamp = 0.01*img_id;
      vo_->addImage(img, timestamp);
      first = false;
      continue;
    }

    cv::Mat img(cv::imread(filename, 0));
    if(img.empty()) {
      // assume sequence ended
      break;
    }

    double timestamp = 0.01*img_id;
    vo_->addImage(img, timestamp);

    if(vo_->lastFrame() != NULL)
    {
      std::cout << "Frame-Id: " << vo_->lastFrame()->id_ << " \t"
                << "#Features: " << vo_->lastNumObservations() << " \t"
                << "Proc. Time: " << vo_->lastProcessingTime()*1000 << "ms \n";
    }
  }
}

} // namespace svo

int main(int argc, char** argv)
{
  if(argc < 2)
  {
    std::cout << "Usage: test_pipeline_kitty <kitti_sequence_dir> [start] [end]" << std::endl;
    std::cout << "The tool expects images in <kitti_sequence_dir>/image_0/000000.png format by default." << std::endl;
    return 1;
  }

  std::string dataset_dir(argv[1]);
  int start = 0;
  int end = 10000;
  if(argc >= 3) start = atoi(argv[2]);
  if(argc >= 4) end = atoi(argv[3]);

  // default pattern matches KITTI odometry: image_0/%06d.png
  std::string pattern = "image_0/%06d.png";

  svo::BenchmarkNodeKITTI benchmark;
  benchmark.runFromFolder(dataset_dir, pattern, start, end);
  std::cout << "BenchmarkNodeKITTI finished." << std::endl;
  return 0;
}
