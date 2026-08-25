/**
 * Backup: stage this project's irreplaceable files, then mirror them to drive B.
 *
 * Run with `node scripts/backup.mjs`. A Windows scheduled task runs it daily at 12:45.
 *
 * Two different jobs, deliberately kept separate:
 *
 *   Stage     Copy the irreplaceable working material into backup/. This project
 *             has no live database, so there is nothing to export from a server.
 *             What it has instead is working material that exists nowhere else:
 *             IR decks that cannot be re-downloaded, pre-edit baselines, the
 *             governing specification, and the pass record. See SOURCES below
 *             for what is included and, just as importantly, what is not.
 *
 *   Mirror    Copy everything in backup/ to B:\Claude Backup\Equity Research\,
 *             then read both copies back and compare hashes. A mirror protects
 *             against losing the C: drive. It does not protect against bad data,
 *             which is why nothing here is ever deleted.
 *
 * Nothing here deletes anything. If the drive is missing or a copy fails, it says
 * so and exits non-zero, leaving what is already on disk alone.
 */

import { createHash } from 'node:crypto'
import { exec } from 'node:child_process'
import { promisify } from 'node:util'
import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const execAsync = promisify(exec)

// ---- CONFIG ----------------------------------------------------------------
const PROJECT = path.resolve(fileURLToPath(import.meta.url), '..', '..')
const LOCAL = path.join(PROJECT, 'backup')
const DUMPS = path.join(LOCAL, 'db')
const REMOTE = 'B:\\Claude Backup\\Equity Research'
const DATABASE = null   // no live database in this project: nothing to export
const PUSH = false      // origin NTRS-ZIB/equity-research is PUBLIC and stays public.
                        // A daily automatic push would publish every future commit
                        // unattended. Pushing here stays a manual choice.
const ALLOW_PUBLIC_PUSH = false
const LOG = path.join(LOCAL, 'backup.log')

/** What gets staged into backup/, and why.
 *
 *  The test is not "is this important" but "can this be fetched again". Anything
 *  re-downloadable is deliberately left out: mirroring it daily costs disk and
 *  buys nothing, because the internet already holds a copy.
 *
 *  from  path relative to the project root
 *  to    path relative to backup/
 */
const SOURCES = [
	// Every file sitting directly in the project root: the published deliverables,
	// the governing specification HOUSE_STYLE.md, the templates, HARNESS_BASELINE.md,
	// CLAUDE.md, README.md, index.html and .gitignore. topOnly, so this does not
	// recurse into the folders listed separately below, nor into backup/ itself.
	//
	// This entry is the one that protects work in progress. PUSH is false and the
	// tracked deliverables only reach GitHub when the owner pushes by hand, so an
	// edit made today and not yet committed exists on the C: drive and nowhere
	// else until this runs.
	{ from: '.', to: '.', topOnly: true },

	// The nine IR presentation decks of 20 Aug 2026. NOT re-downloadable: the
	// issuer URLs are live addresses overwritten in place when the next deck
	// ships, and none of these are on EDGAR. They are the evidence behind 43
	// shipped corrections, so losing them leaves those corrections unverifiable.
	{ from: 'harness/AA_decks_2026-08-20', to: 'harness/AA_decks_2026-08-20' },

	// The verification harness itself: hand-written checks and their repairs, plus
	// the registries recording what has been retrieved and when. Filtered to code
	// and registries only, so the 49 MB of AA_* EDGAR snapshots beside them are
	// left out. Those are re-fetchable from EDGAR, where accessions are immutable.
	{ from: 'harness', to: 'harness', filter: harnessFilter },

	// Each deliverable as it stood before a pass's first edit. The only baselines
	// their passes have, and not reconstructible from the published documents.
	{ from: 'preserve', to: 'preserve' },
	{ from: 'preserved', to: 'preserved' },

	// The as-received originals, under the .received-<date>. naming convention.
	// Marked in .gitignore as never published and never overwritten.
	{ from: '_source_snapshots', to: '_source_snapshots' },

	// Findings, results, conformance and register documents: the written record of
	// what each pass found and repaired. Gitignored by folder, so held nowhere else.
	{ from: 'pass_documentation', to: 'pass_documentation' },

	// Inbound third-party research, licensed and not freely re-obtainable.
	{ from: 'reports', to: 'reports' },

	// Snapshots of the governing specification. Gitignored deliberately, so the
	// repository holds only the hash record in SPEC_VERSIONS.md, not the prose.
	{ from: 'spec_snapshots', to: 'spec_snapshots' },

	// Working material for passes in progress. Despite the name this also holds
	// finished records that were never moved to pass_documentation/, including
	// OUTSTANDING_v196.md, OUTSTANDING_v197.md and two dark-mode RESULTS documents.
	// None of it came from the internet, so none of it can be fetched again.
	{ from: 'scratch', to: 'scratch', filter: notBuildOutput },

	// Local tooling permissions. Small, and annoying to reconstruct from memory.
	{ from: '.claude/settings.local.json', to: '.claude/settings.local.json' },

	// This script itself. It is the thing that knows which files matter and where
	// they go, so restoring everything else without it would leave the next person
	// guessing at the list. It is untracked, so git is not holding a copy either.
	{ from: 'scripts', to: 'scripts' },
]

/** Harness code and registries, not the fetched EDGAR material sitting beside it.
 *  AA_* is the naming convention for a fetched source snapshot; everything else in
 *  that folder was written here. AA_decks_ is the one exception, staged in full
 *  above, because those files cannot be fetched again. */
function harnessFilter(relative) {
	const asPosix = relative.replace(/\\/g, '/')
	const [head, ...rest] = asPosix.split('/')
	const isDirectory = rest.length > 0

	if (asPosix.endsWith('.pyc') || asPosix.includes('__pycache__')) return false

	// Bulk EDGAR download caches. clsk_dl/ is 50 MB of 118 files whose filenames
	// are their own sec.gov Archives URLs, and dl_* are the same thing loose in
	// harness/. An EDGAR accession is permanent and immutable, so every one of
	// these can be fetched again from an address already recorded in its name.
	// This is precisely the "never mirror re-downloadable bulk" case.
	//
	// Note what is NOT excluded here: dated captures of live pages, such as
	// *_ir_coverage_*.html and the press-release and news captures. Those pages
	// change and vanish, so a capture of one is a source that cannot be retaken.
	if (head === 'clsk_dl' || head.startsWith('dl_')) return false

	// Match on the FIRST path segment, not the basename. Testing the basename
	// would exclude a fetched file sitting loose in harness/ but quietly admit a
	// whole AA_ folder of them, because a document inside AA_FOO/ is named
	// something else entirely. That is how AA_BTDR_sweep_2026-08-07 first got in
	// here by accident rather than by decision.
	if (!head.startsWith('AA_')) return true

	// AA_ folders are excluded as a class, so a future sweep of filings does not
	// silently add hundreds of megabytes. These two are admitted deliberately:
	//
	//   AA_decks_2026-08-20   staged by its own SOURCES entry above, so excluded
	//                         here only to avoid staging every file twice.
	//   AA_BTDR_sweep_...     948 KB, and its MANIFEST.txt, LISTING.txt and
	//                         accession lists are work product rather than a
	//                         plain download.
	if (isDirectory) return head.startsWith('AA_BTDR_sweep_')

	// A loose AA_ file in harness/ is a single fetched EDGAR document. EDGAR
	// accessions are permanent and immutable, so these can always be fetched again.
	return false
}

/** Compiled Python is regenerated from the .py beside it on the next run. */
function notBuildOutput(relative) {
	return !relative.endsWith('.pyc') && !relative.includes('__pycache__')
}
// ----------------------------------------------------------------------------

/** Local calendar date as YYYY-MM-DD. Not UTC: a dated file is named for the day
 *  the user had, not the day Greenwich had. */
function today() {
	const now = new Date()
	const pad = (n) => String(n).padStart(2, '0')
	return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`
}

const lines = []
function say(message) {
	console.log(message)
	lines.push(`${new Date().toISOString()}  ${message}`)
}

async function sha256(file) {
	return createHash('sha256').update(await fs.readFile(file)).digest('hex')
}

/** The first line of a failure that actually says something. exec puts the real
 *  complaint on stderr, but npx prints its own install notices there first, and
 *  reporting one of those as the cause sends the reader down the wrong path. */
function reason(error) {
	// Strip colour codes: tools write them to stderr even when not on a terminal,
	// and they arrive in the log as unreadable escape sequences.
	const text = (error.stderr || error.message || String(error)).replace(/\u001b\[[0-9;]*m/g, '')
	const useful = text
		.split('\n')
		.map((line) => line.trim())
		.find((line) => line && !/^npm (warn|notice|err)/i.test(line))
	return (useful || text.split('\n')[0] || 'unknown error').trim()
}

async function exists(target) {
	try {
		await fs.access(target)
		return true
	} catch {
		return false
	}
}

/** PRIVATE, PUBLIC, INTERNAL, or UNKNOWN if it cannot be established. Asks
 *  GitHub rather than trusting anything cached locally, because the answer can
 *  change after setup without a single local file changing. */
async function originVisibility(git) {
	try {
		const url = await git('remote get-url origin')
		// gh.exe, not gh: PowerShell blocks the shim on this machine.
		const { stdout } = await execAsync(`gh.exe repo view ${url} --json visibility -q .visibility`, {
			cwd: PROJECT,
			timeout: 60_000,
		})
		return stdout.trim().toUpperCase() || 'UNKNOWN'
	} catch {
		return 'UNKNOWN'
	}
}

/** Dump the live database to a dated file. Returns the path, or null if the
 *  export failed, or true when there is nothing to snapshot. A failure here must
 *  not stop the mirror: existing files still deserve copying. Left in place with
 *  DATABASE = null, since the summary below reads its result. */
async function snapshotDatabase() {
	if (!DATABASE) {
		say('snapshot: no database configured for this project, skipping')
		return true
	}

	await fs.mkdir(DUMPS, { recursive: true })
	const out = path.join(DUMPS, `${DATABASE}-${today()}.sql`)

	// Export to a scratch name and rename only once it is known good: rename is
	// atomic, so a file at the dated path always means a finished export, which is
	// what the skip below is entitled to assume.
	const partial = `${out}.partial`

	if (await exists(out)) {
		say(`snapshot: already have today's dump, leaving it alone`)
		return out
	}

	say(`snapshot: exporting ${DATABASE} from Cloudflare`)
	try {
		await fs.rm(partial, { force: true })

		// One command string through the shell, rather than execFile with an args
		// array. Two Windows quirks force this: PowerShell refuses the bare `npx`
		// .ps1 shim, and since Node 18.20 spawning a .cmd without a shell fails
		// with EINVAL. Passing an args array alongside shell: true is deprecated,
		// so the command is assembled and quoted here instead.
		await execAsync(
			`npx.cmd wrangler d1 export ${DATABASE} --remote --output "${partial}" -y`,
			{ cwd: PROJECT, timeout: 300_000 },
		)

		const { size } = await fs.stat(partial)
		if (size === 0) throw new Error('export produced an empty file')

		await fs.rename(partial, out)
		say(`snapshot: wrote ${path.basename(out)} (${size} bytes)`)
		return out
	} catch (error) {
		// Leave no debris. A stray .partial must never outlive the run that made it,
		// or a later run could mistake it for real data.
		await fs.rm(partial, { force: true })
		say(`snapshot FAILED: ${reason(error)}`)
		say('snapshot: continuing to the mirror anyway, so existing files still get copied')
		return null
	}
}

/** Every file under a root, as paths relative to that root. */
async function listFiles(root, prefix = '') {
	const found = []
	let entries
	try {
		entries = await fs.readdir(path.join(root, prefix), { withFileTypes: true })
	} catch {
		return found
	}
	for (const entry of entries) {
		const relative = path.join(prefix, entry.name)
		if (entry.isDirectory()) found.push(...(await listFiles(root, relative)))
		// Skip the log, and skip any .partial left by a run that died between
		// writing and the rename. Half a file is not worth mirroring.
		else if (entry.name !== path.basename(LOG) && !entry.name.endsWith('.partial')) found.push(relative)
	}
	return found
}

/** Copy one file only when the destination differs, then verify by reading back.
 *  Returns 'copied' or 'unchanged', or throws. */
async function copyVerified(from, to) {
	const before = await sha256(from)
	const unchanged = (await exists(to)) && (await sha256(to)) === before
	if (!unchanged) {
		await fs.mkdir(path.dirname(to), { recursive: true })
		await fs.copyFile(from, to)
	}
	// Read the destination back rather than trusting the copy. This is the whole
	// point of the exercise: an unverified backup is a guess.
	if ((await sha256(to)) !== before) throw new Error('hash mismatch after copy')
	return unchanged ? 'unchanged' : 'copied'
}

/** Stage the irreplaceable working material listed in SOURCES into backup/.
 *
 *  This project's equivalent of a database export. What it protects is not on a
 *  server to be exported; it is working files that live in the project and exist
 *  nowhere else. Staging them into backup/ gives the mirror below something to
 *  carry, and keeps backup/ a single self-contained answer to the question
 *  "what would I actually miss".
 *
 *  Nothing is deleted here. A file removed from the project stays in backup/ and
 *  on drive B, which is deliberate: an accidental delete is one of the failures a
 *  backup exists to survive. */
async function stageSources() {
	let copied = 0
	let unchanged = 0
	const failures = []

	for (const source of SOURCES) {
		const from = path.join(PROJECT, source.from)
		if (!(await exists(from))) {
			say(`stage: ${source.from} does not exist, skipping`)
			continue
		}

		const isDirectory = (await fs.stat(from)).isDirectory()

		// topOnly takes the files sitting directly in the folder and does not
		// recurse. For the project root that matters twice over: recursing would
		// pull in the whole tree including the 49 MB of EDGAR snapshots this list
		// deliberately excludes, and it would walk backup/ into itself.
		let relatives
		if (!isDirectory) relatives = [null]
		else if (source.topOnly) {
			relatives = (await fs.readdir(from, { withFileTypes: true }))
				.filter((entry) => entry.isFile())
				.map((entry) => entry.name)
		} else relatives = await listFiles(from)

		for (const relative of relatives) {
			if (source.filter && relative !== null && !source.filter(relative)) continue
			const fromFile = relative === null ? from : path.join(from, relative)
			const toFile = relative === null ? path.join(LOCAL, source.to) : path.join(LOCAL, source.to, relative)
			// Per file, so one locked or unreadable file is recorded as a failure
			// rather than aborting the loop and silently skipping everything after it.
			try {
				const result = await copyVerified(fromFile, toFile)
				if (result === 'copied') copied += 1
				else unchanged += 1
			} catch (error) {
				failures.push(`${source.from}/${relative ?? ''} (${error.code || error.message})`)
			}
		}
	}

	say(`stage: ${copied} copied, ${unchanged} already current`)
	for (const bad of failures) say(`stage FAILED: ${bad}`)
	return failures.length === 0
}

/** Copy backup/ to drive B and verify by hashing both sides. */
async function mirror() {
	// Two CONFIG mistakes that would otherwise crash obscurely or pass silently.
	//
	// The placeholder: Windows rejects < and > in a path, so leaving it in surfaces
	// as a bare ENOENT from mkdir, reading like a broken drive.
	//
	// Single backslashes: 'B:\Claude Backup\Foo' is not a syntax error in JS, it
	// quietly becomes "B:Claude BackupFoo" because \C and \F are not escape
	// sequences. That writes a real folder in the wrong place and then reports
	// success, which is the worst possible outcome for a backup.
	if (REMOTE.includes('<')) {
		say(`mirror FAILED: REMOTE is still the placeholder, edit CONFIG (${REMOTE})`)
		return false
	}
	if (!REMOTE.startsWith('B:\\Claude Backup\\')) {
		say('mirror FAILED: REMOTE must sit under B:\\Claude Backup\\ and needs')
		say(`  doubled backslashes in the string. Got: ${REMOTE}`)
		return false
	}

	// A missing drive is the difference between "backed up" and "not backed up",
	// so treat it as a hard failure rather than a warning nobody reads.
	if (!(await exists('B:\\'))) {
		say('mirror FAILED: drive B is not attached, nothing was copied')
		return false
	}

	await fs.mkdir(REMOTE, { recursive: true })
	const files = await listFiles(LOCAL)

	// An empty backup/ is the quiet failure this whole exercise exists to prevent.
	// Without this guard the loop below runs zero times, finds zero failures, and
	// the run reports "OK: drive B mirrored" over nothing at all. Every acceptance
	// test would pass: exit code 0, a fresh log line, the expected push message.
	// A backup that lies about its own health is worse than none.
	if (files.length === 0) {
		say('mirror FAILED: backup/ is empty, so there is nothing to mirror.')
		say('  Staging must have failed or SOURCES is misconfigured. Refusing to')
		say('  report success over an empty backup.')
		return false
	}

	let copied = 0
	let matched = 0
	const failures = []

	for (const relative of files) {
		const from = path.join(LOCAL, relative)
		const to = path.join(REMOTE, relative)

		// Per file, so one locked or unreadable file is recorded as a failure
		// rather than aborting the loop and silently skipping everything after it.
		try {
			const result = await copyVerified(from, to)
			if (result === 'copied') copied += 1
			matched += 1
		} catch (error) {
			failures.push(`${relative} (${error.code || error.message})`)
		}
	}

	say(`mirror: ${files.length} files, ${copied} copied, ${matched} verified identical`)
	for (const bad of failures) say(`mirror FAILED to verify: ${bad}`)
	return failures.length === 0
}

/** Push commits already made to the GitHub repo.
 *
 *  This deliberately does not commit anything. Committing on a timer would sweep
 *  up half-finished work, and worse, could publish a file the author had not yet
 *  decided to track. Only work the author already chose to commit gets sent, and
 *  never with --force. */
async function pushCommits() {
	if (!PUSH) {
		say('push: disabled in CONFIG for this project')
		return true
	}

	const git = async (command) => (await execAsync(`git ${command}`, { cwd: PROJECT })).stdout.trim()

	try {
		if (!(await git('remote'))) {
			say('push: no GitHub remote configured, skipping')
			return true
		}

		// Refuse to publish to the world on a timer.
		//
		// A setup session checks visibility once, by hand, at setup time. This task
		// then runs every day for years. If origin is public, every commit the
		// author ever makes is published unattended within a day, including one that
		// accidentally contains a key. The one-time scan cannot see a secret that
		// does not exist yet, so the guard has to live here.
		//
		// Unknown counts as refuse. If gh cannot answer, the safe assumption is the
		// one that does not publish.
		const visibility = await originVisibility(git)
		if (visibility !== 'PRIVATE' && !ALLOW_PUBLIC_PUSH) {
			say(`push REFUSED: origin visibility is ${visibility}, not PRIVATE.`)
			say('  A daily automatic push would publish every future commit.')
			say('  Make the repo private, or set ALLOW_PUBLIC_PUSH in CONFIG if')
			say('  publishing this project really is intended.')
			return false
		}

		// A repo with no commits has no HEAD, and everything below would fail with
		// "ambiguous argument 'HEAD'", which says nothing useful.
		try {
			await git('rev-parse --verify HEAD')
		} catch {
			say('push: no commits in this repository yet, nothing to push')
			return true
		}

		// Uncommitted work is not protected by the push, and the author may not
		// realise. Say so rather than reporting a clean success.
		const dirty = await git('status --porcelain')
		if (dirty) {
			const count = dirty.split('\n').length
			say(`push: note, ${count} uncommitted file(s) in the project are NOT backed up to GitHub`)
		}

		const branch = await git('rev-parse --abbrev-ref HEAD')

		// A branch with no upstream is one the author has never published. An
		// unattended task must not be the thing that publishes it for them: a
		// private scratch branch is exactly where half-finished work and stray
		// credentials live. Report it as unprotected and let them decide.
		const tracked = await git(`branch --list --format=%(upstream) ${branch}`)
		if (!tracked) {
			say(`push: ${branch} has never been pushed, so it is NOT backed up to GitHub.`)
			say(`  Run "git push -u origin ${branch}" yourself once if you want it protected.`)
			return true
		}

		const ahead = await git(`rev-list --count ${tracked}..HEAD`)
		if (ahead === '0') {
			say('push: GitHub is already up to date')
			return true
		}

		say(`push: sending ${ahead} commit(s) to GitHub`)
		await git(`push origin ${branch}`)
		say('push: done')
		return true
	} catch (error) {
		// Offline, or the remote moved ahead. Neither is worth a force-push; the
		// local history and drive B are both still intact.
		say(`push FAILED: ${reason(error)}`)
		return false
	}
}

let dump = null
let staged = false
let mirrored = false
let pushed = false

try {
	dump = await snapshotDatabase()
	staged = await stageSources()
	mirrored = await mirror()
	pushed = await pushCommits()

	if (dump && staged && mirrored && pushed) say('OK: drive B mirrored and everything else up to date')
	else if (mirrored) say('PARTIAL: drive B is up to date, but see the failures above')
	else say('PROBLEM: the mirror did not complete, drive B is not up to date')
} catch (error) {
	// Nothing may escape without reaching the log. The log is the only thing the
	// user reads, so a crash that wrote nothing would leave the previous run's
	// "OK" sitting there as the last line, reading as healthy.
	say(`PROBLEM: the backup crashed before finishing: ${error.message || error}`)
} finally {
	try {
		await fs.mkdir(LOCAL, { recursive: true })
		await fs.appendFile(LOG, lines.join('\n') + '\n')
	} catch (error) {
		// The log itself is unwritable. Nowhere left to record that, but the
		// non-zero exit below still reaches the scheduled task's LastTaskResult.
		console.error(`could not write ${LOG}: ${error.message}`)
	}
}

process.exit(dump && staged && mirrored && pushed ? 0 : 1)
