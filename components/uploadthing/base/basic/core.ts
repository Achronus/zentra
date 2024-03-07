import { createUploadthing, type FileRouter } from 'uploadthing/server';

const f = createUploadthing();

// Template auth function
const authenticateUser = (req: Request) => ({ id: "fakeId" });

// FileRouter for your app, can contain multiple FileRoutes
export const uploadFileRouter = {
  // Define as many FileRoutes as you like, each with a unique routeSlug
  media: f({ image: { maxFileSize: '4MB', maxFileCount: 1 } })
    .middleware(authenticateUser)
    .onUploadComplete(() => {}),
} satisfies FileRouter;

export type UploadFileRouter = typeof uploadFileRouter;
