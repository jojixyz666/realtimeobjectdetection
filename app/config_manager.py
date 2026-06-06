import argparse
import yaml
import os

class ConfigManager:
    def __init__(self, default_config_path="config.yaml"):
        self.config = self._load_yaml(default_config_path)
        self._parse_cli_args()

    def _load_yaml(self, path):
        if not os.path.exists(path):
            print(f"Warning: Config file {path} not found. Using empty defaults.")
            return {}
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading YAML config: {e}")
            return {}

    def _parse_cli_args(self):
        parser = argparse.ArgumentParser(description="Realtime Object Detection")
        parser.add_argument("--source", type=str, help="Source input (0 for webcam, file path, RTSP URL)")
        parser.add_argument("--model", type=str, help="Path to model file (.pt)")
        parser.add_argument("--conf", type=float, help="Confidence threshold")
        parser.add_argument("--iou", type=float, help="IOU threshold")
        parser.add_argument("--imgsz", type=int, help="Inference image size")
        parser.add_argument("--device", type=str, help="Device (cpu, cuda, mps, auto)")
        parser.add_argument("--classes", type=int, nargs='+', help="Filter classes (e.g., 0 2 5)")
        parser.add_argument("--save-video", action="store_true", help="Save output as video")
        parser.add_argument("--save-img", action="store_true", help="Save frames as images")
        parser.add_argument("--save-json", action="store_true", help="Save logs as JSON")
        parser.add_argument("--output-dir", type=str, help="Output directory path")
        parser.add_argument("--show", action="store_true", help="Show display window")
        parser.add_argument("--config", type=str, help="Path to custom config.yaml")
        parser.add_argument("--verbose", action="store_true", help="Verbose logging")

        args = parser.parse_args()

        # If a custom config is provided, load it and overwrite current dict
        if args.config:
            custom_cfg = self._load_yaml(args.config)
            self._merge_dicts(self.config, custom_cfg)

        # Merge CLI args into config dictionary
        if 'model' not in self.config:
            self.config['model'] = {}
        if args.model:
            self.config['model']['path'] = args.model
        if args.conf is not None:
            self.config['model']['conf_threshold'] = args.conf
        if args.iou is not None:
            self.config['model']['iou_threshold'] = args.iou
        if args.imgsz is not None:
            self.config['model']['imgsz'] = args.imgsz
        if args.device:
            self.config['model']['device'] = args.device

        if 'source' not in self.config:
            self.config['source'] = {}
        if args.source is not None:
            self.config['source']['input'] = args.source

        if 'filter' not in self.config:
            self.config['filter'] = {}
        if args.classes is not None:
            self.config['filter']['classes'] = args.classes

        if 'output' not in self.config:
            self.config['output'] = {}
        if args.save_video:
            self.config['output']['save_video'] = True
        if args.save_img:
            self.config['output']['save_images'] = True
        if args.save_json:
            self.config['output']['save_json'] = True
        if args.output_dir:
            self.config['output']['output_dir'] = args.output_dir
        # Only override if explicitly provided, for simplicity in bool args we might need careful handling, 
        # but args.show acts as a flag. If it's provided, set to True, though config might have it True by default.
        if args.show:
            self.config['output']['show_window'] = True

        if 'logging' not in self.config:
            self.config['logging'] = {}
        if args.verbose:
            self.config['logging']['level'] = "DEBUG"

    def _merge_dicts(self, dict1, dict2):
        for k, v in dict2.items():
            if isinstance(v, dict) and k in dict1 and isinstance(dict1[k], dict):
                self._merge_dicts(dict1[k], v)
            else:
                dict1[k] = v

    def get(self, section, key=None, default=None):
        if key is None:
            return self.config.get(section, default)
        return self.config.get(section, {}).get(key, default)
