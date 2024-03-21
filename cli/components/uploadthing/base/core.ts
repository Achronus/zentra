import { createUploadthing, type FileRouter } from 'uploadthing/next';
import { auth } from '@clerk/nextjs';

const f = createUploadthing();

// Only allow authenticated user to upload files
const authenticateUser = () => {
  const user = auth();
  // If you throw, the user will not be able to upload
  if (!user) throw new Error('Unauthorized');
  // Whatever is returned here is accessible in onUploadComplete as `metadata`
  return user;
}

// FileRouter for your app, can contain multiple FileRoutes
export const uploadFileRouter = {
  // Define as many FileRoutes as you like, each with a unique routeSlug
  avatar: f({ image: { maxFileSize: '4MB', maxFileCount: 1 } })
    .middleware(authenticateUser)
    .onUploadComplete(() => {}),
    
  media: f({ image: { maxFileSize: '4MB', maxFileCount: 1 } })
    .middleware(authenticateUser)
    .onUploadComplete(() => {}),
} satisfies FileRouter;

export type UploadFileRouter = typeof uploadFileRouter;
