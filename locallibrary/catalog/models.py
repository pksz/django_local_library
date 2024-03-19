from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
import uuid

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]

class Book(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey('Author',on_delete=models.RESTRICT,null=True)
    summary=models.TextField(max_length=1000,help_text="a breif description about the book")
    isbn=models.CharField('ISBN',
                          max_length=13,
                          unique=True,
                          help_text="ISBN NUMBER")
    
    genre=models.ManyToManyField(Genre,help_text="select a genre")

    language=models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)

    def __str__(self):
          return self.title


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('book-detail', args=[str(self.id)])


    class Meta:
        ordering = ['title', 'author']


class BookInstance(models.Model):
    Id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="unique id representing each book")
    book=models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    imprint=models.CharField(max_length=200,blank=True)
    due_back=models.DateField(null=True,blank=True)

    LOAN_STATUS=(
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    staus=models.CharField(max_length=1,
                           choices=LOAN_STATUS,
                           blank=True,
                           default='m',
                           help_text='book availability')
    
    class Meta:
         ordering=['due_back']

    def __str__(self):
         return f'{self.id}({self.book.title})'
    


class Author(models.Model):
    first_name=models.CharField(max_length=100,blank=False)
    last_name=models.CharField(max_length=100,blank=False)
    date_of_birth=models.DateField(blank=True,null=True)
    date_of_death=models.DateField('Died',blank=True,null=True)
     
    class Meta:
        ordering=['last_name','first_name']
    
    
    def get_absolute_url(self):
        return reverse('author_detail',args=[str(self.id)])
    
    def __str__(self) -> str:
         return f'{self.first_name}{self.last_name}'


class Language(models.Model):
    name=models.CharField(max_length=50,
                           unique=True,
                           help_text='language of the book')
    def get_absolute_url(self):
         return reverse('language_detail',args=[str(self.id)])
    
    def __str__(self) -> str:
         return self.name