_base_ = [
    '../../_base_/models/slowfast_r50.py', '../../_base_/default_runtime.py'
]

# model settings
model = dict(
    cls_head=dict(
        type='SlowFastHead',
        num_classes=30
        ))

dataset_type = 'VideoDataset'
data_root = "/cluster/home/t125959uhn/Data/Kimia'sProject-HHExperimentsRecordings_compressed"
data_root_val = "/cluster/home/t125959uhn/Data/Kimia'sProject-HHExperimentsRecordings_compressed"
ann_file_train = "/cluster/home/t125959uhn/Data/Kimia'sProject-HHExperimentsRecordings_compressed/30_70/2/train.txt"
ann_file_val = "/cluster/home/t125959uhn/Data/Kimia'sProject-HHExperimentsRecordings_compressed/30_70/2/val.txt"
ann_file_test = "/cluster/home/t125959uhn/Data/Kimia'sProject-HHExperimentsRecordings_compressed/30_70/2/test.txt"

file_client_args = dict(io_backend='disk')
train_pipeline = [
    dict(type='DecordInit', **file_client_args),
    dict(type='SampleFrames', clip_len=64, frame_interval=5, num_clips=1),
    dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='RandomResizedCrop'),
    dict(type='Resize', scale=(224, 224), keep_ratio=False),
    dict(type='Flip', flip_ratio=0.5),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='PackActionInputs')
]
val_pipeline = [
    dict(type='DecordInit', **file_client_args),
    dict(
        type='SampleFrames',
        clip_len=64,
        frame_interval=5,
        num_clips=1,
        test_mode=True),
    dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='CenterCrop', crop_size=224),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='PackActionInputs')
]
test_pipeline = [
    dict(type='DecordInit', **file_client_args),
    dict(
        type='SampleFrames',
        clip_len=64,
        frame_interval=5,
        num_clips=10,
        test_mode=True),
    dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='ThreeCrop', crop_size=256),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='PackActionInputs')
]
train_dataloader = dict(
    batch_size=32,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        data_prefix=dict(video=data_root),
        pipeline=train_pipeline))
val_dataloader = dict(
    batch_size=32,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_test,
        data_prefix=dict(video=data_root_val),
        pipeline=val_pipeline,
        test_mode=True))
test_dataloader = dict(
    batch_size=1,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_test,
        data_prefix=dict(video=data_root_val),
        pipeline=test_pipeline,
        test_mode=True))

val_evaluator = dict(type='AccMetric')
test_evaluator = val_evaluator

train_cfg = dict(
    type='EpochBasedTrainLoop', max_epochs=100, val_begin=1, val_interval=3)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

optim_wrapper = dict(
    optimizer=dict(type='SGD', lr=0.005, momentum=0.9, weight_decay=1e-4),
    clip_grad=dict(max_norm=40, norm_type=2))

param_scheduler = [
    dict(
        type='LinearLR',
        start_factor=0.1,
        by_epoch=True,
        begin=0,
        end=34,
        convert_to_iter_based=True),
    dict(
        type='CosineAnnealingLR',
        T_max=256,
        eta_min=0,
        by_epoch=True,
        begin=0,
        end=256)
]

default_hooks = dict(
    checkpoint=dict(interval=4, max_keep_ckpts=1), logger=dict(interval=100))
