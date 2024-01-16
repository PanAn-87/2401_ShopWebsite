from app01.models import Tag

def tag_data(request):
    tag_list = Tag.objects.all()
    return {"tag_list": tag_list}