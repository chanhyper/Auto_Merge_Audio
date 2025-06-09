import os
import argparse
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def adjust_volume(audio: AudioSegment, target_dBFS: float) -> AudioSegment:
    """
    调整音频音量至目标分贝值
    
    参数:
        audio (AudioSegment): 要调整的音频段
        target_dBFS (float): 目标分贝值
    
    返回:
        AudioSegment: 调整后的音频段
    """
    try:
        # 计算需要调整的分贝差值
        dBFS_diff = target_dBFS - audio.dBFS
        # 应用音量调整
        return audio.apply_gain(dBFS_diff)
    except Exception as e:
        logger.error(f"音量调整失败: {e}")
        # 如果调整失败，返回原始音频
        return audio


def merge_audio_files(cn_dir: str, en_dir: str, output_dir: str, volume_sync: bool = False, target_dBFS: float = -20.0) -> None:
    """
    合并中英文音频文件
    
    参数:
        cn_dir (str): 中文音频目录路径
        en_dir (str): 英文音频目录路径
        output_dir (str): 输出目录路径
        volume_sync (bool): 是否同步音量
        target_dBFS (float): 目标音量分贝值
    
    返回:
        None
    """
    try:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取文件列表并按数字排序
        cn_files = sorted([f for f in os.listdir(cn_dir) if f.endswith('.mp3')], 
                         key=lambda x: int(x.split('.')[0]))
        en_files = sorted([f for f in os.listdir(en_dir) if f.endswith('.mp3')], 
                         key=lambda x: int(x.split('.')[0]))
        
        # 验证文件数量匹配
        if len(cn_files) != len(en_files):
            logger.warning(f"中英文文件数量不匹配: 中文{len(cn_files)}个, 英文{len(en_files)}个")
        
        # 处理每对音频文件
        for i, (cn_file, en_file) in enumerate(zip(cn_files, en_files), 1):
            cn_path = os.path.join(cn_dir, cn_file)
            en_path = os.path.join(en_dir, en_file)
            # 根据实际情况修改输出文件名
            output_path = os.path.join(output_dir, f"merged_{cn_file}")
            
            try:
                # 加载音频文件
                cn_audio = AudioSegment.from_mp3(cn_path)
                en_audio = AudioSegment.from_mp3(en_path)
                
                # 如果启用音量同步，调整两个音频的音量
                if volume_sync:
                    logger.info(f"同步音量至 {target_dBFS} dBFS")
                    cn_audio = adjust_volume(cn_audio, target_dBFS)
                    en_audio = adjust_volume(en_audio, target_dBFS)
                    logger.info(f"调整后音量 - 中文: {cn_audio.dBFS:.2f} dBFS, 英文: {en_audio.dBFS:.2f} dBFS")
                
                # 合并音频（先中文后英文）
                merged_audio = cn_audio + en_audio
                
                # 导出合并后的文件
                merged_audio.export(output_path, format="mp3")
                # 根据实际情况修改输出文件名
                logger.info(f"成功合并: {cn_file} + {en_file} → merged_{cn_file}")
                
            except CouldntDecodeError:
                logger.error(f"文件解码失败: {cn_path} 或 {en_path}")
            except Exception as e:
                logger.error(f"处理文件时出错: {e}")
                
    except Exception as e:
        logger.error(f"程序运行失败: {e}")

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="合并中英文音频文件")
    parser.add_argument("--cn_dir", default="cn", help="中文音频目录路径")
    parser.add_argument("--en_dir", default="en", help="英文音频目录路径")
    parser.add_argument("--output_dir", default="output", help="输出目录路径")
    parser.add_argument("--volume_sync", action="store_true", help="是否同步音量")
    parser.add_argument("--target_dBFS", type=float, default=-20.0, help="目标音量分贝值")
    args = parser.parse_args()
    
    # 配置路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CN_DIR = os.path.join(BASE_DIR, args.cn_dir)
    EN_DIR = os.path.join(BASE_DIR, args.en_dir)
    OUTPUT_DIR = os.path.join(BASE_DIR, args.output_dir)
    
    # 执行合并
    merge_audio_files(CN_DIR, EN_DIR, OUTPUT_DIR, args.volume_sync, args.target_dBFS)