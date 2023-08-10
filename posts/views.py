from users.models import User
from .models import Post,Comment
from .permissions import CustomReadOnly
from .serializers import PostSerializer, PostCreateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

### CRUD 구현
### 게시판 분류를 어떻게 할 지 정해야 시작가능할 듯
### url로 나눌 것인지, ?category={id} 등으로 받아올 것인지...
