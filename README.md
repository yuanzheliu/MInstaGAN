# Refine on InstaGAN

## How to run the code on AWS:
1. Installation(注意requirements.txt里面的torch使用torch == 1.4.0): 
```pip install -r requirements.txt```
2. Download CCP dataset: 
```git clone https://github.com/bearpaw/clothing-co-parsing ./datasets/clothing-co-parsing```
3. Generate two-domain datasets: 
```python ./datasets/generate_ccp_dataset.py --save_root ./datasets/jeans2skirt_ccp --cat1 jeans --cat2 skirt```
4. ssh 链接 aws: 
```ssh -i aws_key -L 8000:localhost:8097 ubuntu@xxx```
5. 建一个tmux session 启动 visdom: 
```python -m visdom.server```
6. 再建一个tmux session train model：
```python train.py --dataroot ./datasets/jeans2skirt_ccp --model insta_gan --name jeans2skirt_ccp_instagan --loadSizeH 330 --loadSizeW 220 --fineSizeH 300 --fineSizeW 200 --niter 30 --niter_decay 200  --batch_size 100```
7. 本地登陆visdom 看train实时结果

## Reference
[InstaGAN](https://github.com/sangwoomo/instagan) PyTorch implementation of ["InstaGAN: Instance-aware Image-to-Image Translation"](https://openreview.net/forum?id=ryxwJhC9YX) (ICLR 2019).
The implementation is based on the [official CycleGAN](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix) code.

## Citation
```
@inproceedings{
    mo2019instagan,
    title={InstaGAN: Instance-aware Image-to-Image Translation},
    author={Sangwoo Mo and Minsu Cho and Jinwoo Shin},
    booktitle={International Conference on Learning Representations},
    year={2019},
    url={https://openreview.net/forum?id=ryxwJhC9YX},
}
```
