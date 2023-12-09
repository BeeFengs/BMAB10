from sd_bmab.base.context import Context

from sd_bmab.detectors.person import UltralyticsPersonDetector8m
from sd_bmab.detectors.person import UltralyticsPersonDetector8n, UltralyticsPersonDetector8s
from sd_bmab.detectors.face import UltralyticsFaceDetector8n, UltralyticsFaceDetector8s
from sd_bmab.detectors.face import UltralyticsFaceDetector8nv2, UltralyticsFaceDetector8m
from sd_bmab.detectors.face import BmabFaceSmall, BmabFaceNormal
from sd_bmab.detectors.hand import UltralyticsHandDetector8n, UltralyticsHandDetector8s
from sd_bmab.util import debug_print


def get_detector(context: Context, model: str, **kwargs):

	debug_print('model', model)
	if model == 'face_yolov8n.pt':
		return UltralyticsFaceDetector8n(**kwargs)

	all_detectors = [
		BmabFaceNormal(**kwargs),
		BmabFaceSmall(**kwargs),
		UltralyticsPersonDetector8m(**kwargs),
		UltralyticsPersonDetector8n(**kwargs),
		UltralyticsPersonDetector8s(**kwargs),
		UltralyticsFaceDetector8n(**kwargs),
		UltralyticsFaceDetector8nv2(**kwargs),
		UltralyticsFaceDetector8m(**kwargs),
		UltralyticsFaceDetector8s(**kwargs),
		UltralyticsHandDetector8n(**kwargs),
		UltralyticsHandDetector8s(**kwargs),
	]

	targets = [x for x in all_detectors if model == x.target()]
	if len(targets) == 1:
		return targets[0]
	raise Exception(f'Not found or multiple detector {model}')


def list_person_detectors():
	kwargs = {}
	person_detectors = [
		UltralyticsPersonDetector8m(**kwargs),
		UltralyticsPersonDetector8n(**kwargs),
		UltralyticsPersonDetector8s(**kwargs),
	]
	return [x.target() for x in person_detectors]


def list_face_detectors():
	kwargs = {}
	face_detectors = [
		BmabFaceNormal(**kwargs),
		BmabFaceSmall(**kwargs),
		UltralyticsFaceDetector8n(**kwargs),
		UltralyticsFaceDetector8nv2(**kwargs),
		UltralyticsFaceDetector8m(**kwargs),
		UltralyticsFaceDetector8s(**kwargs),
	]
	return [x.target() for x in face_detectors]


def list_hand_detectors():
	kwargs = {}
	hand_detectors = [
		UltralyticsHandDetector8n(**kwargs),
		UltralyticsHandDetector8s(**kwargs),
	]
	return [x.target() for x in hand_detectors]
