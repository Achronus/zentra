import { createRouteHandler } from 'uploadthing/next';

import { uploadFileRouter } from './core';

export const { GET, POST } = createRouteHandler({
    router: uploadFileRouter 
});
