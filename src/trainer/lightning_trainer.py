import logging
import time

import pytorch_lightning as pl
from pytorch_lightning.callbacks import TQDMProgressBar
from pytorch_lightning.loggers import TensorBoardLogger
from src.utils.cuda_status import get_num_gpus

logger = logging.getLogger(__name__)

def setup_logger(exp_name,version=None):
    """
    setup tensorbard logs,
    save_dir='tensorboard_logs'
    """
    pl_logger = TensorBoardLogger(
        save_dir='tensorboard_logs',
        name=exp_name,
        version=version,
        )
    return pl_logger

def get_trainer(args, version=None, precision=32, fast_dev_run=False):
    if args.no_cuda:
        accelerator = 'cpu'
        logger.info(f'[Trainer] CUDA disable by no_cuda flag')
    else:
        accelerator = 'auto'
        logger.info(f'[Trainer] number of GPU found {get_num_gpus()}')

    pb_cb = TQDMProgressBar(refresh_rate=1)
    
    trainer = pl.Trainer(
        accelerator=accelerator,
        devices='auto',
        fast_dev_run=fast_dev_run,
        precision=precision,
        max_epochs=args.epochs,
        logger=setup_logger(f'{args.model}_{args.dataset}_fold={args.fold}_{time.strftime("%Y-%m-%d-%H:%M:%S")}', version),
        callbacks=[pb_cb],
    )
    return trainer
