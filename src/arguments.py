"""Common arguments for train and evaluation for CFENet"""
import argparse


def cfenet_arguments():
    """Arguments used for both training and testing"""
    parser = argparse.ArgumentParser(add_help=False)

    # Logging
    parser.add_argument(
        "--logdir",
        default="../logs",
        type=str,
        help="Directory to store logs, summaries, checkpoints.",
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="If true, will ignore logdir and log to ../logdev instead",
    )
    parser.add_argument("--name", type=str, help="Prefix to add to logging directory")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="If set, will enable autograd anomaly detection",
    )
    # settings for input data_loader
    parser.add_argument(
        "-i",
        "--dataset_path",
        default="../datasets/modelnet40_ply_hdf5_2048",
        type=str,
        metavar="PATH",
        help="path to the processed dataset. Default: ../datasets/modelnet40_ply_hdf5_2048",
    )
    parser.add_argument(
        "--dataset_type",
        default="modelnet_hdf",
        choices=[
            "modelnet_hdf",
            "kitti_odometry",
            "bunny",
            "armadillo",
            "buddha",
            "dragon",
        ],
        metavar="DATASET",
        help="dataset type (default: modelnet_hdf)",
    )
    parser.add_argument(
        "--num_points",
        default=1024,
        type=int,
        metavar="N",
        help="points in point-cloud (default: 1024)",
    )
    parser.add_argument(
        "--noise_type",
        default="crop_scale",
        choices=["clean", "jitter", "crop", "crop_scale", "crop_scale_dense", "kitti"],
        help="Types of perturbation to consider",
    )
    parser.add_argument(
        "--rot_mag",
        default=45.0,
        type=float,
        metavar="T",
        help="Maximum magnitude of rotation perturbation (in degrees)",
    )
    parser.add_argument(
        "--trans_mag",
        default=0.5,
        type=float,
        metavar="T",
        help="Maximum magnitude of translation perturbation",
    )
    parser.add_argument(
        "--partial",
        default=[0.7, 0.7],
        nargs="+",
        type=float,
        help="Approximate proportion of points to keep for partial overlap (Set to 1.0 to disable)",
    )
    # Model
    parser.add_argument(
        "--method",
        type=str,
        default="cfenet",
        choices=["cfenet", "fgr", "ransac", "icp", "dcp_v2", "rpmnet", "dgr"],
        help="Model to use. Note: Only cfenet is supported for training."
        "'eye' denotes identity (no registration), 'gt' denotes groundtruth transforms",
    )
    # PointNet settings
    parser.add_argument(
        "--radius",
        type=float,
        default=0.3,
        help="Neighborhood radius for computing pointnet features",
    )
    parser.add_argument(
        "--num_neighbors",
        type=int,
        default=64,
        metavar="N",
        help="Max num of neighbors to use",
    )
    # CFENet settings
    parser.add_argument(
        "--features",
        type=str,
        choices=["ppf", "dxyz", "xyz"],
        default=["ppf", "dxyz", "xyz"],
        nargs="+",
        help="Which features to use. Default: all",
    )
    parser.add_argument(
        "--feat_dim",
        type=int,
        default=96,
        help="Feature dimension (to compute distances on). Other numbers will be scaled accordingly",
    )
    parser.add_argument("--feat_ball_dim", type=int, default=72)
    parser.add_argument(
        "--no_slack", action="store_true", help="If set, will not have a slack column."
    )
    parser.add_argument(
        "--num_sk_iter",
        type=int,
        default=5,
        help="Number of inner iterations used in sinkhorn normalization",
    )
    parser.add_argument(
        "--num_reg_iter",
        type=int,
        default=5,
        help="Number of outer iterations used for registration (only during inference)",
    )
    parser.add_argument(
        "--loss_type",
        type=str,
        choices=["mse", "mae", "l1"],
        default="mae",
        help="Loss to be optimized",
    )
    parser.add_argument(
        "--wt_inliers", type=float, default=1e-2, help="Weight to encourage inliers"
    )
    # Training parameters
    parser.add_argument(
        "--train_batch_size",
        default=16,
        type=int,
        metavar="N",
        help="training mini-batch size (default 8)",
    )
    parser.add_argument(
        "-b",
        "--val_batch_size",
        default=1,
        type=int,
        metavar="N",
        help="mini-batch size during validation or testing (default: 16)",
    )
    parser.add_argument(
        "--resume",
        default=None,
        type=str,
        metavar="PATH",
        help="Pretrained network to load from. Optional for train, required for inference.",
    )
    parser.add_argument(
        "--gpu",
        default="0",
        type=str,
        metavar="DEVICE",
        help="GPU to use, ignored if no GPU is present. Set to negative to use cpu",
    )

    # METHOD OPTIONS, defaults all should be proposed
    parser.add_argument(
        "--sk_type",
        type=str,
        default="sum_approx",
        choices=["sum", "log", "sum_approx", "log_approx"],
    )
    parser.add_argument("--via_cpu", action="store_true")
    parser.add_argument(
        "--ppf_type", type=str, default="inner_prod", choices=["inner_prod", "angle"]
    )
    parser.add_argument(
        "--knn",
        type=str,
        default="k_select",
        choices=[
            "k_select",
            "topk",
            "topk_select",
            "all_sort",
            "in_radius",
            "faiss_k_select",
            "faiss_topk",
        ],
    )
    parser.add_argument("--scale_min", type=float, default=0)
    parser.add_argument("--scale_max", type=float, default=0)
    parser.add_argument("--scale_test", type=float, default=0)

    return parser


def cfenet_train_arguments():
    """Used only for training"""
    parser = argparse.ArgumentParser(parents=[cfenet_arguments()])

    parser.add_argument(
        "--train_categoryfile",
        type=str,
        metavar="PATH",
        default="./data_loader/modelnet40_half1.txt",
        help="path to the categories to be trained",
    )  # eg. './dataset/modelnet40_half1.txt'
    parser.add_argument(
        "--val_categoryfile",
        type=str,
        metavar="PATH",
        default="./data_loader/modelnet40_half1.txt",
        help="path to the categories to be val",
    )  # eg. './sampledata/modelnet40_half1.txt'
    # Training parameters
    parser.add_argument(
        "--lr", default=1e-4, type=float, help="Learning rate during training"
    )
    parser.add_argument(
        "--param_lr", default=5e-5, type=float, help="Learning rate during training"
    )
    parser.add_argument("--param_betas", nargs="*", default=[0.9, 0.999], type=float)
    parser.add_argument("--weight_decay", default=1e-7, type=float)
    parser.add_argument("--gamma", default=1.0, type=float)
    parser.add_argument("--milestones", nargs="*", default=[600, 800])

    parser.add_argument(
        "--epochs",
        default=1000,
        type=int,
        metavar="N",
        help="number of total epochs to run",
    )
    parser.add_argument(
        "--summary_every",
        default=200,
        type=int,
        metavar="N",
        help="Frequency of saving summary (number of steps if positive, number of epochs if negative)",
    )
    parser.add_argument(
        "--validate_every",
        default=-4,
        type=int,
        metavar="N",
        help="Frequency of evaluation (number of steps if positive, number of epochs if negative)."
        "Also saves checkpoints at the same interval",
    )
    parser.add_argument(
        "--num_workers",
        default=8,
        type=int,
        help="Number of workers for data_loader loader (default: 4).",
    )

    # 自分で追加したやつら
    parser.add_argument("--min_points", default=1024, type=int)
    parser.add_argument("--max_points", default=1024, type=int)

    parser.description = "Train CFENet"
    return parser


def cfenet_eval_arguments():
    """Used during evaluation"""
    parser = argparse.ArgumentParser(parents=[cfenet_arguments()])

    # settings for input data_loader
    parser.add_argument(
        "--test_category_file",
        type=str,
        metavar="PATH",
        default="./data_loader/modelnet40_half2.txt",
        help="path to the categories to be val",
    )
    # Provided transforms
    parser.add_argument(
        "--transform_file",
        type=str,
        help="If provided, will use transforms from this provided pickle file",
    )
    # Save out evaluation data_loader for further analysis
    parser.add_argument(
        "--eval_save_path",
        type=str,
        default="../eval_results",
        help="Output data_loader to save evaluation results",
    )
    parser.add_argument("--save_pics", action="store_true")
    parser.description = "CFENet evaluation"
    return parser
