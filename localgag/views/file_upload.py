from rest_framework.decorators import api_view
from uuid import uuid4

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


# @api_view(['POST'])
# # @permission_classes((IsAuthenticated, ))
# def upload_file(request):
#     file = request.FILES['file']
#
#     uuid = uuid4()
#
#     return Response({"filename": "hello"}, status=HTTP_200_OK)
from rest_framework.views import APIView


class FileUploadView(APIView):

    parser_classes = (FileUploadParser, )

    accepted_images = ['jpg', 'jpeg', 'png', 'gif']
    accepted_videos = ['']

    def post(self, request, filename):
        file = request.data['file']

        file_format = filename.split('.')[-1]

        if file_format in self.accepted_images:
            with open('{}.{}'.format(uuid4(), file_format), 'w'):
                pass

        return Response(status=HTTP_200_OK)


upload_file = FileUploadView.as_view()
