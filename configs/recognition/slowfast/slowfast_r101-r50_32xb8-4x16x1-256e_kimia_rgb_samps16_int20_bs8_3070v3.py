_base_ = ['slowfast_r50_8xb8-4x16x1-256e_kimia_rgb_samps16_int20_bs8_3070v3.py']

model = dict(backbone=dict(slow_pathway=dict(depth=101)))

optim_wrapper = dict(optimizer=dict(lr=0.005 * 4))
