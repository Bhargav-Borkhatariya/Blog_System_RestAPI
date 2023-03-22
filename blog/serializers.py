from rest_framework import serializers
from blog.models import BlogPost, Category

class BlogSerializer(serializers.ModelSerializer):
    
    # Specify that category is a CharField instead of CategorySerializer
    category = serializers.CharField()

    class Meta:
        model = BlogPost
        fields = ('id', 'author', 'title',
                  'content', 'category', 'image',
                  'status', 'created_on', 'updated_on')
        read_only_fields = ('id', 'author', 'created_on', 'updated_on')

    def create(self, validated_data):
        # Get the category data from validated_data and remove it from the dict
        category_data = validated_data.pop('category')
        
        # Get or create the Category object using the category name
        category = Category.objects.get_or_create(name=category_data)[0]
        
        # Create the BlogPost object with the category and validated_data
        blog = BlogPost.objects.create(category=category, **validated_data)
        return blog
    

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.status = validated_data.get('status', instance.status)
        instance.image = validated_data.get('image', instance.image)

        # Retrieve the Category instance using the provided category name
        category_name = validated_data.get('category', instance.category.name)
        category = Category.objects.get(name=category_name)
        instance.category = category

        instance.save()
        return instance
