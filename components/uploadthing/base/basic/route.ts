import { createRouteHandler } from 'uploadthing/server';

import { uploadFileRouter } from "~/server/uploadthing";

export const { GET, POST } = createRouteHandler({
    router: uploadFileRouter,
    config: {
        uploadthingSecret: import.meta.env.UPLOADTHING_SECRET,
    },
});
