const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
require("date-format-lite");

const mysql = require("mysql2");

const port = 1337;
const app = express();

/* =======================
   Middleware
======================= */
app.use(express.static(path.join(__dirname, "public")));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

/* =======================
   MySQL Pool (GLOBAL)
======================= */
const db = mysql.createPool({
  host: "localhost",
  user: "souren",
  password: "Nylon#365",
  database: "gantt_chart_test"
}).promise();

/* =======================
   Routes
======================= */

// GET all data
app.get("/data", async (req, res) => {
  try {
    const [tasks] = await db.query("SELECT * FROM gantt_tasks");
    const [links] = await db.query("SELECT * FROM gantt_links");

    tasks.forEach(task => {
      task.start_date = task.start_date.format("YYYY-MM-DD hh:mm:ss");
      task.open = true;
    });

    res.send({
      data: tasks,
      collections: { links }
    });
  } catch (error) {
    sendResponse(res, "error", null, error);
  }
});

// INSERT task
app.post("/data/task", async (req, res) => {
  try {
    const task = getTask(req.body);

    const [result] = await db.query(
      "INSERT INTO gantt_tasks (text, start_date, duration, progress, parent) VALUES (?,?,?,?,?)",
      [task.text, task.start_date, task.duration, task.progress, task.parent]
    );

    sendResponse(res, "inserted", result.insertId);
  } catch (error) {
    sendResponse(res, "error", null, error);
  }
});

// UPDATE task
app.put("/data/task/:id", async (req, res) => {
  try {
    const sid = req.params.id;
    const task = getTask(req.body);

    await db.query(
      "UPDATE gantt_tasks SET text=?, start_date=?, duration=?, progress=?, parent=? WHERE id=?",
      [task.text, task.start_date, task.duration, task.progress, task.parent, sid]
    );

    sendResponse(res, "updated");
  } catch (error) {
    sendResponse(res, "error", null, error);
  }
});

// DELETE task
app.delete("/data/task/:id", async (req, res) => {
  try {
    await db.query("DELETE FROM gantt_tasks WHERE id=?", [req.params.id]);
    sendResponse(res, "deleted");
  } catch (error) {
    sendResponse(res, "error", null, error);
  }
});

// INSERT link
app.post("/data/link", async (req, res) => {
  try {
    const link = getLink(req.body);

    const [result] = await db.query(
      "INSERT INTO gantt_links (source, target, type) VALUES (?,?,?)",
      [link.source, link.target, link.type]
    );

    sendResponse(res, "inserted", result.insertId);
  } catch (error) {
    sendResponse(res, "error", null, error);
  }
});

// UPDATE link
app.put("/data/link/:id", async (req, res) => {
  try {
    const sid = req.params.id;
    const link = getLink(req.body);

    await db.query(
      "UPDATE gantt_links SET source=?, target=?, type=? WHERE id=?",
      [link.source, link.target, link.type, sid]
    );

    sendResponse(res, "updated");
  } catch (error) {
    sendResponse(res, "error", null, error);
  }
});

// DELETE link
app.delete("/data/link/:id", async (req, res) => {
  try {
    await db.query("DELETE FROM gantt_links WHERE id=?", [req.params.id]);
    sendResponse(res, "deleted");
  } catch (error) {
    sendResponse(res, "error", null, error);
  }
});

/* =======================
   Helpers
======================= */
function sendResponse(res, action, tid = null, error = null) {
  if (error) console.error(error);

  const result = { action };
  if (tid !== null) result.tid = tid;

  res.send(result);
}

function getTask(data) {
  return {
    text: data.text,
    start_date: new Date(data.start_date).format("YYYY-MM-DD"),
    duration: data.duration,
    progress: data.progress || 0,
    parent: data.parent
  };
}

function getLink(data) {
  return {
    source: data.source,
    target: data.target,
    type: data.type
  };
}

/* =======================
   Start Server
======================= */
app.listen(port, () => {
  console.log(`Server is running on port ${port}...`);
});
