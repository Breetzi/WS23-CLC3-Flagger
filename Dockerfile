FROM python:3
WORKDIR /app
ADD app /app
	
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]