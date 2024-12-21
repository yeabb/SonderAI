from django.db import models
from django.contrib.auth.models import User

class TweetNode(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="tweets", 
        help_text="The user who created the tweet."
    )  # Cascading on deletion to prevent orphan records in DB
    title = models.CharField(
        max_length=25, 
        help_text="Short title to the post (max 25 characters)."
    )
    content = models.TextField(
        max_length=280, 
        help_text="The text content of the tweet (max 280 characters)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="The timestamp when the tweet was created."
    )  
    updated_at = models.DateTimeField(
        auto_now=True, 
        help_text="The timestamp when the tweet was last updated."
    )
    parent_node = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="child_tweets", 
        help_text="The parent node of the thread if this is part of a thread."
    )
    liked_by = models.ManyToManyField(
        User, 
        related_name='liked_posts', 
        blank=True, 
        help_text="Users who liked this tweet."
    )
    retweeted_by = models.ManyToManyField(
        User, 
        related_name='retweeted_tweets', 
        blank=True, 
        help_text="Users who retweeted this tweet."
    )
    number_of_likes = models.PositiveIntegerField(
        default=0, 
        help_text="The number of likes the tweet has."  # Cached count
    )
    number_of_retweets = models.PositiveBigIntegerField(
        default=0, 
        help_text="The number of retweets the tweet has."  # Cached count
    )
    is_retweet = models.BooleanField(
        default=False, 
        help_text="Indicates whether this is a retweet."
    )
    original_tweet = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="retweets_set", 
        help_text="Reference to the original tweet if this is a retweet."
    )
    replies = models.ManyToManyField(
        'self', 
        symmetrical=False,
        blank=True, 
        related_name="parent_tweets", 
        help_text="Replies to this tweet."
    )

    def __str__(self):
        return f"Tweet by {self.user.username}: {self.content[:50]}"

    class Meta:
        ordering = ['-created_at']  # Default order by most recent
        verbose_name = "Tweet Node"
        verbose_name_plural = "Tweet Nodes"

    # Methods for likes and retweets
    def like(self, user):
        """Add a like from a user."""
        if not self.liked_by.filter(id=user.id).exists():
            self.liked_by.add(user)
            self.number_of_likes = self.liked_by.count()
            self.save()

    def unlike(self, user):
        """Remove a like from a user."""
        if self.liked_by.filter(id=user.id).exists():
            self.liked_by.remove(user)
            self.number_of_likes = self.liked_by.count()
            self.save()

    def retweet(self, user):
        """Add a retweet from a user."""
        if not self.retweeted_by.filter(id=user.id).exists():
            self.retweeted_by.add(user)
            self.number_of_retweets = self.retweeted_by.count()
            self.save()

    def undo_retweet(self, user):
        """Remove a retweet from a user."""
        if self.retweeted_by.filter(id=user.id).exists():
            self.retweeted_by.remove(user)
            self.number_of_retweets = self.retweeted_by.count()
            self.save()
