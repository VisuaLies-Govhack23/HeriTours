import * as crypto from 'crypto';
import * as esbuild from 'esbuild';
import * as fs from 'fs';

const NO_WATCH = !process.argv.includes('--watch');
const MINIFY = process.argv.includes('--minify');

const RAW_FILES: Record<string, string> = {
    'index.html': 'index.html'
};

const digestCache: Record<string, string> = {};
function isChanged(filename: string): boolean {
    const hash = crypto.createHash('sha256');
    const body = fs.readFileSync(filename);
    hash.update(body);
    const digest = hash.digest('hex');

    const isChanged = digestCache[filename] !== digest;
    digestCache[filename] = digest;

    return isChanged;
}

async function build() {
    fs.mkdirSync(`./dist/ui/static`, { recursive: true });

    // Raw files to copy as-is
    for (const [target, source] of Object.entries(RAW_FILES)) {
        const sourcePath = `./frontend/${source}`;
        const targetPath = `./dist/ui/static/${target}`;
        const raw = fs.readFileSync(sourcePath);
        fs.writeFileSync(targetPath, raw);

        if (!NO_WATCH) {
            fs.watch(sourcePath, () => {
                if (isChanged(sourcePath)) {
                    const raw = fs.readFileSync(sourcePath);
                    fs.writeFileSync(targetPath, raw);
                    console.log(target, 'rebuilt.');
                }
            });
        }
    }

    // JavaScript Front-end
    const context = await esbuild.context({
        entryPoints: {
            index: './frontend/index.tsx'
        },
        bundle: true,
        minify: MINIFY,
        outdir: './dist/ui/js',
        platform: 'browser',
        sourcemap: !MINIFY,
        target: 'es2015',
        plugins: [
            {
                name: 'logger',
                setup(build) {
                    build.onEnd(() => {
                        console.log('frontend build complete.');
                    });
                }
            }
        ]
    });

    if (NO_WATCH) {
        await context.rebuild();
        await context.dispose();
    } else {
        await context.watch();
    }
}

build()
    .then(() => {
        // pass
    })
    .catch(e => {
        console.error(e);
    });
