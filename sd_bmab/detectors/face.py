import torch
from PIL import Image
from ultralytics import YOLO

import modules
from modules import images
from modules import shared

from sd_bmab import util
from sd_bmab.base.context import Context
from sd_bmab.base.detectorbase import DetectorBase


class FaceDetector(DetectorBase):

	def description(self):
		return f'Face detecting using {self.target()}'


class UltralyticsFaceDetector(FaceDetector):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
		self.confidence = kwargs.get('box_threshold', 0.35)
		self.model = None

	def target(self):
		return f'Ultralytics({self.model})'

	def predict(self, context: Context, image: Image):
		yolo = util.lazy_loader(self.model)
		boxes = []
		confs = []
		load = torch.load
		torch.load = modules.safe.unsafe_torch_load
		try:
			model = YOLO(yolo)
			pred = model(image, conf=self.confidence, device='')
			boxes = pred[0].boxes.xyxy.cpu().numpy()
			boxes = boxes.tolist()
			confs = pred[0].boxes.conf.tolist()
		except:
			pass
		torch.load = load
		return boxes, confs


class UltralyticsFaceDetector8n(UltralyticsFaceDetector):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
		self.model = 'face_yolov8n.pt'


class UltralyticsFaceDetector8m(UltralyticsFaceDetector):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
		self.model = 'face_yolov8m.pt'


class UltralyticsFaceDetector8nv2(UltralyticsFaceDetector):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
		self.model = 'face_yolov8n_v2.pt'


class UltralyticsFaceDetector8s(UltralyticsFaceDetector):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
		self.model = 'face_yolov8s.pt'


class BmabFaceSmall(UltralyticsFaceDetector):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
		self.model = 'bmab_face_sm_yolov8n.pt'

	def target(self):
		return 'BMAB Face(Small)'

	def predict(self, context: Context, image: Image):
		if shared.opts.bmab_debug_logging:
			boxes, logits = super().predict(context, image)
			if len(boxes) == 0:
				images.save_image(
					image, context.sdprocessing.outpath_samples, '',
					context.sdprocessing.all_seeds[context.index], context.sdprocessing.all_prompts[context.index],
					shared.opts.samples_format, p=context.sdprocessing, suffix="-debugging")
				det = UltralyticsFaceDetector8n()
				return det.predict(context, image)
			return boxes, logits
		else:
			return super().predict(context, image)


class BmabFaceNormal(UltralyticsFaceDetector):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
		self.model = 'bmab_face_nm_yolov8n.pt'

	def target(self):
		return 'BMAB Face(Normal)'

	def predict(self, context: Context, image: Image):
		if shared.opts.bmab_debug_logging:
			boxes, logits = super().predict(context, image)
			if len(boxes) == 0:
				images.save_image(
					image, context.sdprocessing.outpath_samples, '',
					context.sdprocessing.all_seeds[context.index], context.sdprocessing.all_prompts[context.index],
					shared.opts.samples_format, p=context.sdprocessing, suffix="-debugging")
				det = UltralyticsFaceDetector8n()
				return det.predict(context, image)
			return boxes, logits
		else:
			return super().predict(context, image)





