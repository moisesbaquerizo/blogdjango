from django import forms
from blogs.models import Post, Comment, Rating

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'overview', 'content', 'categorias', 'image']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Agregar clases a los widgets de cada campo
        self.fields['title'].widget.attrs.update({
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
        self.fields['slug'].widget.attrs.update({
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
        })
        self.fields['overview'].widget.attrs.update({
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
        self.fields['categorias'].widget.attrs.update({
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })


class PostCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='Ingrese comentario')

    class Meta:
        model = Comment
        fields = ['content']

class SuperPostForm(PostForm):
    featured = forms.BooleanField(required=False, label='Publicar como destacado')

    class Meta(PostForm.Meta):
        fields = PostForm.Meta.fields + ['featured']

    def __init__(self, *args, **kwargs):
        super(SuperPostForm, self).__init__(*args, **kwargs)
        self.fields['featured'].widget.attrs.update({
            'class': 'form-checkbox h-5 w-5 text-blue-600 transition duration-150 ease-in-out'
        })

