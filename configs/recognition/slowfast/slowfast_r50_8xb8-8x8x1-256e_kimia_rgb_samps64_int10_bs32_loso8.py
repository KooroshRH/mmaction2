_base_ = ['slowfast_r50_8xb8-4x16x1-256e_kimia_rgb_samps64_int10_bs32_loso8.py']

model = dict(
    backbone=dict(
        resample_rate=4,  # tau
        speed_ratio=4,  # alpha
        channel_ratio=8,  # beta_inv
        slow_pathway=dict(fusion_kernel=7)))
