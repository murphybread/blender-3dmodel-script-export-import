# blender-3dmodel-script-export-import

개요
현재 3d모델을 코드로 사용한다면 나중에 AI로 학습시켜서 복잡한 구조물도 만들 수 있을거 같아서 만들어본 스크립트
## export
python기반으로 blender의 모델의 필요한 값을들 json으로 현재 블렌더파일 위치에 저장합니다.
기본적으로 mesh에서 사용하는 vertex, edge ,face의 값들을 저장합니다.
추가적으로 texture가 있는 경우 uv 좌표와 함께 파일로 새로만듭니다.


## import
export에의해 약속된 파일이름을 통해 json으로 부터 여러 오브젝트들의 mesh를 만듭니다.
텍스쳐의 경우 단순한게 아닌 복잡한 텍스쳐를 상정해서 이미 저장해놓은 텍스쳐파일을 적용하는 방식으로 구현했습니다.
