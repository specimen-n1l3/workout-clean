import cv2
from typing import Any, Dict, List, Tuple
import numpy as np
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

WHITE = (0, 0, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LEFTSHOULDER = 6 #the keypoint in posenet
LEFTELBOW = 8
LEFTWRIST = 10



def keypoint_coords(keypoint: List[float], image_size: Tuple[int, int]) -> List[int]:
   
   width, height = image_size[0], image_size[1]
   x, y = keypoint
   x *= width
   y *= height


   return int(x), int(y)

def draw_text(img, x, y, text_str: str, color_code):
   """Helper function to call opencv's drawing function,
   to improve code readability in node's run() method.
   """
   cv2.putText(
      img=img,
      text=text_str,
      org=(x, y),
      fontFace=cv2.FONT_HERSHEY_SIMPLEX,
      fontScale=0.4,
      color=color_code,
      thickness=2,
   )

class Node(AbstractNode):

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)




    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        keypoints = inputs["keypoints"]
        x1, y1 = keypoint_coords(keypoints[LEFTSHOULDER])
        x2, y2 = keypoint_coords(keypoints[LEFTELBOW])
        x3, y3 = keypoint_coords(keypoints[LEFTWRIST])
        line1 = np.array([x1, y1, x2, y2])
        line2 = np.array([x2, y2, x3, y3])
        angle = cv2.phase(line1, line2, angleInDegrees=True)
        if angle is not None:
            draw_text(img, 0, 0, "You're doing good", GREEN)

        return {}

        

