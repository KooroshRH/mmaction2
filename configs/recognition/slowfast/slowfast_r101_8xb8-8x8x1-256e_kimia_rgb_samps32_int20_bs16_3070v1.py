_base_ = ['slowfast_r50_8xb8-8x8x1-256e_kimia_rgb_samps32_int20_bs16_3070v1.py']

model = dict(
    backbone=dict(slow_pathway=dict(depth=101), fast_pathway=dict(depth=101)))
