# blender-3dmodel-script-export-import

현재 선태된 3d모델들을 json파일로 export한 후, 이 json 파일을 import하여 구현하는 두개의 스크립트들입니다.

# export.py
python기반으로 blender의 모델의 필요한 값을들 json으로 현재 블렌더파일 위치에 `exported_objects.json`파일 저장합니다.
기본적으로 선택된 mesh들 에서 사용하는 vertex, edge ,face의 값들을 저장합니다.
사용된 텍스처 이미지는 textures 폴더에 PNG 형식으로 저장합니다.
추가적으로 texture가 있는 경우 uv 좌표와 함께 파일로 새로만듭니다.


# import.py
export에의해 `exported_objects.json`으로 부터 여러 오브젝트들의 mesh를 만듭니다.
텍스쳐의 경우 단순한게 아닌 복잡한 텍스쳐를 상정해서 이미 저장해놓은 텍스쳐파일을 적용하는 방식으로 구현했습니다.


---

Personal

목적: 블렌더 스크립트 기능 학습

결과: 여러 메쉬들을 크고 복잡한 동작이 아닌 가볍고 단순한 파일 하나로 관리 가능

