/**
 * Google Workspace MCP — Apps Script Backend
 *
 * 배포 방법:
 * 1. Google Drive → 새로 만들기 → Google Apps Script
 * 2. 이 파일의 전체 내용을 복사-붙여넣기
 * 3. 배포 → 새 배포 → 웹 앱
 *    - 실행 계정: "나" (배포자)
 *    - 액세스 권한: "조직 내 누구나" (도메인 제한)
 * 4. 배포 URL을 복사하여 MCP setup 도구에 입력
 */

function doPost(e) {
  try {
    var request = JSON.parse(e.postData.contents);
    var action = request.action;
    var userEmail = request.userEmail;

    switch (action) {
      case "ping":
        return jsonResponse({ ok: true, message: "Apps Script 연결 성공" });

      case "readDocument":
        return jsonResponse(readDocument(request.docId));

      case "inspectTemplate":
        return jsonResponse(inspectTemplate(request.docId));

      case "copyTemplate":
        return jsonResponse(
          copyTemplate(
            request.templateDocId,
            request.title,
            userEmail,
            request.folderId
          )
        );

      case "fillFields":
        return jsonResponse(fillFields(request.docId, request.fields));

      case "getShareLink":
        return jsonResponse(
          getShareLink(request.docId, request.access, request.role)
        );

      default:
        return jsonResponse({ error: "알 수 없는 action: " + action });
    }
  } catch (err) {
    return jsonResponse({ error: err.message || String(err) });
  }
}

function doGet() {
  return ContentService.createTextOutput(
    "Google Workspace MCP Backend is running."
  );
}

// --- Helper ---

function jsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data)).setMimeType(
    ContentService.MimeType.JSON
  );
}

// --- Actions ---

/**
 * Read the full text content of a Google Doc.
 */
function readDocument(docId) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  return {
    docId: docId,
    title: doc.getName(),
    text: body.getText(),
  };
}

/**
 * Extract all {{placeholder}} fields from a template.
 */
function inspectTemplate(docId) {
  var doc = DocumentApp.openById(docId);
  var text = doc.getBody().getText();
  var regex = /\{\{([^}]+)\}\}/g;
  var match;
  var placeholders = [];
  var seen = {};

  while ((match = regex.exec(text)) !== null) {
    if (!seen[match[1]]) {
      placeholders.push(match[1]);
      seen[match[1]] = true;
    }
  }

  placeholders.sort();
  return {
    docId: docId,
    title: doc.getName(),
    placeholders: placeholders,
    count: placeholders.length,
  };
}

/**
 * Copy a template, fill nothing yet, transfer ownership to user.
 */
function copyTemplate(templateDocId, title, userEmail, folderId) {
  var templateFile = DriveApp.getFileById(templateDocId);
  var copy;

  if (folderId) {
    var folder = DriveApp.getFolderById(folderId);
    copy = templateFile.makeCopy(title, folder);
  } else {
    copy = templateFile.makeCopy(title);
  }

  // Transfer ownership to the user (same domain required)
  copy.setOwner(userEmail);

  return {
    docId: copy.getId(),
    title: title,
    owner: userEmail,
    url: copy.getUrl(),
  };
}

/**
 * Fill {{placeholder}} fields and report unfilled ones.
 */
function fillFields(docId, fields) {
  var doc = DocumentApp.openById(docId);
  var body = doc.getBody();
  var replacedCount = 0;

  var keys = Object.keys(fields);
  for (var i = 0; i < keys.length; i++) {
    var placeholder = "{{" + keys[i] + "}}";
    var found = body.findText(placeholder.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    if (found) {
      body.replaceText(
        placeholder.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
        fields[keys[i]]
      );
      replacedCount++;
    }
  }

  doc.saveAndClose();

  // Scan for remaining unfilled placeholders
  doc = DocumentApp.openById(docId);
  var remaining = [];
  var text = doc.getBody().getText();
  var regex = /\{\{([^}]+)\}\}/g;
  var match;
  var seen = {};

  while ((match = regex.exec(text)) !== null) {
    if (!seen[match[1]]) {
      remaining.push(match[1]);
      seen[match[1]] = true;
    }
  }

  return {
    docId: docId,
    fieldsProvided: keys.length,
    replacementsApplied: replacedCount,
    unfilledFields: remaining.sort(),
    unfilledCount: remaining.length,
  };
}

/**
 * Set sharing permissions and return the share link.
 */
function getShareLink(docId, access, role) {
  var file = DriveApp.getFileById(docId);
  var domain = Session.getEffectiveUser().getEmail().split("@")[1];

  if (access === "domain") {
    // Share with entire domain
    if (role === "writer") {
      file.setSharing(DriveApp.Access.DOMAIN_WITH_LINK, DriveApp.Permission.EDIT);
    } else if (role === "commenter") {
      file.setSharing(DriveApp.Access.DOMAIN_WITH_LINK, DriveApp.Permission.COMMENT);
    } else {
      file.setSharing(DriveApp.Access.DOMAIN_WITH_LINK, DriveApp.Permission.VIEW);
    }
  } else {
    // Share with anyone with link
    if (role === "writer") {
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
    } else if (role === "commenter") {
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.COMMENT);
    } else {
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    }
  }

  return {
    docId: docId,
    url: file.getUrl(),
    access: access,
    role: role,
    domain: domain,
  };
}
