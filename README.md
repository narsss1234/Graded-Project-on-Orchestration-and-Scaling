# SampleMERNwithMicroservices

### Solution

Step 1: Set Up the AWS Environment

1. Set Up AWS CLI and Boto3:

   - Install AWS CLI and configure it with AWS credentials.

   ```
   aws configure

   aws sts get-caller-identity
   ```

   - Install Boto3 for Python and configure it.

   ```
   pip install boto3
   ```
Step 2: Prepare the MERN Application

1. Containerize the MERN Application:

   - Ensure the MERN application is containerized using Docker. Create a Dockerfile for each component (frontend and backend).

### Backend - helloService Containerization

Checked and found that the index.js file, requires an environment variable for PORT

```
cd backend/helloservice

touch .env

added a variable PORT 4200
```

Created a dockerfile using node:alpine base image

```
touch Dockerfile

EXPOSE 4200

CMD - node index.js  -> as this is backend
```

### Backend - profileService Containerization

Checked and found that the index.js file, requires an environment variable for PORT and also a url for MONGO_URL

```
cd backend/profileService

touch .env

added the port 4400, and also a mongo url
```

Created a Dockerfile expose port 4400

```
EXPOSE 4400

CMD  - node index.ks -> as this is backend
```


### frontend Containerization

As per the README.md file, frontend will be exposed on port 3000

Also in the Home.js file, the backend application url are present change these, so that it can point the correct address and ports.

```
vim src/components/Home.js

added - 

http://localhost:4200/

&

http://localhost:4400/fetchUser
```

Created Dockerfile

```
touch Dockerfile

Expose port 3000

CMD - npm start
```

### Mongo

Created a mongo collection - test

added the below document - 

```

_id
65f478d60b5b79810cf4a80b
name
"sree"
age
"27"
```

### testing the dockerfiles - 

Let's Build the docker files first

# Backend - helloService
```
cd .\backend\helloService\

docker build -t narsss1234/microservice-backend-hello:latest .
```

# Backend - profileService

```
cd .\backend\profileService

docker build -t narsss1234/microservice-backend-profile:latest .
```

# Frontend

```
cd .\frontend

docker build -t narsss1234/microservice-frontend:latest .
```

### application tested locally

![alt text](image.png)

---------------------------------------

2. Push Docker Images to Amazon ECR:

   - Build Docker images for the frontend and backend.

   - Create an Amazon ECR repository for each image.

   - Push the Docker images to their respective ECR repositories.

As the testing is complete lets push the image to dockerhub and also ECR

```
docker push narsss1234/microservice-backend-profile:latest

docker push narsss1234/microservice-backend-hello:latest

docker push narsss1234/microservice-frontend:latest
```
Logged into AWS console - navigated to ECR

Created repos for each - backend 1,2 and frontend

ECR public repos created

![alt text](image-1.png)

```
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 367065853931.dkr.ecr.ap-south-1.amazonaws.com

docker tag narsss1234/microservice-backend-hello:latest 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-backend-hello:latest

docker push 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-backend-hello:latest

docker tag narsss1234/microservice-backend-profile:latest 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-backend-profile:latest

docker push 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-backend-profile:latest

docker tag narsss1234/microservice-frontend:latest 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-frontend:latest

docker push 367065853931.dkr.ecr.ap-south-1.amazonaws.com/microservice-frontend:latest
```

Docker images have been pushed to ECR

