### Build SVO
cd /workspace/rpg_svo/svo
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Debug \
  -DSophus_DIR=/workspace/Sophus/build \
  -Dfast_DIR=/workspace/fast/build \
  -Dvikit_common_DIR=/workspace/rpg_vikit/vikit_common/build ..
make -j$(nproc)

or just run:

/workspace/build_svo

### Set env vars before running test_pipeline
export LD_LIBRARY_PATH=/workspace/rpg_svo/svo/lib:/workspace/rpg_vikit/vikit_common/lib:/workspace/Sophus/build:$LD_LIBRARY_PATH

### Test pipeline:
export SVO_DATASET_DIR=/workspace/datasets
/workspace/rpg_svo/svo/bin/test_pipeline
### Test pipeline KITTI:
/workspace/rpg_svo/svo/bin/test_pipeline_kitty /path/to/kitti/sequence_folder [start] [end]
#### Example: sequence 00, path: /workspace/kitti/dataset/sequences/00:
/workspace/rpg_svo/svo/bin/test_pipeline_kitty /workspace/kitti/dataset/sequences/00 0 100


### Valgrind test_pipeline
valgrind --tool=memcheck --leak-check=full --show-reachable=yes --track-origins=yes --num-callers=20 --error-limit=no --log-file=/workspace/valgrind_test_pipeline_kitty.log /workspace/rpg_svo/svo/bin/test_pipeline_kitty /workspace/kitti/dataset/sequences/00 0 100


## Conda
### Activate
eval "$(/workspace/miniorge3/bin/conda shell.bash hook)"
### TSFormer-VVO
conda create -n tsformer-vo python==3.8.0
conda activate tsformer-vo
### KITTI Odometry Evaluation Toolbox
conda env create -f kitti-odom-eval/requirement.yml -p kitti_eval
conda activate /workspace/kitti_eval
python eval_odom.py --result result/TSformer-VO_model3/ --align scale_7dof
