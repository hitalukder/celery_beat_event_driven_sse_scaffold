# Deploy to openshift container

## Build the container image

### Pre-requisite

- And IBM cloud container registry
- You created a namespace in it

Build container image and push it to the ibm container registry

Login to ibm cloud:

```sh
ibmcloud login --sso
```

login to ibm cloud container registry

```sh
ibmcloud cr login
```

Got to the deployment run directory

```sh
cd deploy/run
```

Modify the script `build_and_push.sh` variables before you run the script

```sh
# --- CONFIGURATION ---
NAMESPACE_NAME="celery-container-registry"
REGISTRY="us.icr.io"
VERSION="v1" # Increment manually when needed

IMAGE_NAME=”” # line 33 & 36
```

Build and push backend image

```sh
./build_and_push.sh backend
```

Build and push frontend image

```sh
./build_and_push.sh frontend
```

Now you have both the backend and frontend images are ready. Lets jump into the next step to deploy all the application and services.

## Deploy backend application in OpenShift cluster.

Login to openshift console and copy login command

<img width="1304" height="524" alt="image" src="https://github.com/user-attachments/assets/f8915da8-dee0-4d59-b7f4-53827229ff38" />

Create a new project or use an existing project.

```sh
oc new-project llm-judge
```

Go to the ocp deployment directory

```sh
cd deploy/ocp/deployment
```

Change and modify configuration in the kustomization.yml file

```sh
vi backend/base/kustomization.yaml
```

Change the `newName` and `newTag` in the image section. 

If necessary change the secretGenerator section as well.

```yml
images:
  - name: backend-image-name
    newName: us.icr.io/htalukder-cr/celery_backend_app
    newTag: 22102025-v2
secretGenerator:
- name: celery-task-secret
  literals:
    - REDIS_URL=redis://redis:6379/0
    - MONGO_URL=mongodb://mongo:27017/
    - DB_NAME=realtime_data
    - PULL_INTERVAL=2.0
    - API_URL=https://jsonplaceholder.typicode.com/todos/
    - STOP_FLAG_KEY=STOP_FLAG_KEY
```

Apply the deployment

```sh
oc apply -k backend/base/
```

Get the backend route

```sh
oc get route
```
