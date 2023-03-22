from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_activation_otp_email(user, otp):
    email_subject = f"Activation OTP for {user}"
    email_body = render_to_string("activation.txt", {"user": user, "otp": otp})
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.send()


def send_forget_password_otp_email(user, otp):
    email_subject = f"Forget Password OTP for {user}"
    email_body = render_to_string("forget_pass.txt", {"user": user, "otp": otp})
    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.send()


def send_posted_comment_email(blog_post, content, commenter):
    email_subject = f"Got Comment On {blog_post}"
    email_body = render_to_string("comment.txt", {
        "author": blog_post.author,
        "post_title": blog_post,
        "content": content,
        "commenter": commenter})
    email = EmailMessage(
        email_subject,
        email_body,
        to=[blog_post.author.email])
    email.send()
