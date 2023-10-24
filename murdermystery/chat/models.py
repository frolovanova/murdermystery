from django.db import models

class ChatMessage(models.Model):
    game_code = models.CharField(max_length=50)
    characterpair = models.CharField(max_length=100)
    sender = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    characterpair = models.CharField(max_length=50, default='')  # Add default value

    class Meta:
        unique_together = ('game_code', 'characterpair')

    def __str__(self):
        return f"{self.sender}: {self.message}"
