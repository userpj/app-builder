package com.baidubce.appbuilder.console.appbuilderclient;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.iterator.StreamIterator;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import com.baidubce.appbuilder.model.appbuilderclient.*;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.*;

import org.apache.hc.client5.http.entity.mime.HttpMultipartMode;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

public class AppBuilderClient extends Component {
    public String appID;

    public AppBuilderClient(String appID) {
        super();
        this.appID = appID;
    }

    public AppBuilderClient(String appID, String secretKey) {
        super(secretKey);
        this.appID = appID;
    }

    public AppBuilderClient(String appID, String secretKey, String gateway) {
        super(secretKey, gateway);
        this.appID = appID;
    }

    /**
     * 创建会话
     *
     * @return 返回会话ID
     * @throws IOException 当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public String createConversation() throws IOException, AppBuilderServerException {
        return innerCreateConversation();
    }

    private String innerCreateConversation() throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CREATE_CONVERSATION_URL;
        if (this.appID == null || this.appID.isEmpty()) {
            throw new RuntimeException("Param 'appID' is required!");
        }
        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("app_id", this.appID);
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<ConversationResponse> response =
                httpClient.execute(postRequest, ConversationResponse.class);
        ConversationResponse respBody = response.getBody();

        return respBody.getConversationId();
    }

    /**
     * 上传本地文件到指定会话中
     *
     * @param conversationId 会话ID
     * @param filePath 文件路径
     * @return 上传后的文件ID
     * @throws IOException 当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public String uploadLocalFile(String conversationId, String filePath)
            throws IOException, AppBuilderServerException {
        return innerUploadLocalFile(conversationId, filePath, "");
    }

    public String uploadFile(String conversationId, String filePath, String fileUrl)
            throws IOException, AppBuilderServerException {
        return innerUploadLocalFile(conversationId, filePath, fileUrl);
    }

    private String innerUploadLocalFile(String conversationId, String filePath, String fileUrl)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.UPLOAD_FILE_URL;
        if (this.appID == null || this.appID.isEmpty()) {
            throw new RuntimeException("Param 'appID' is required!");
        }
        MultipartEntityBuilder builder = MultipartEntityBuilder.create()
                .setMode(HttpMultipartMode.LEGACY).setCharset(StandardCharsets.UTF_8);

        if(filePath != null && !filePath.isEmpty()) {
            builder.addBinaryBody("file", new File(filePath));
        } else if (fileUrl != null && !fileUrl.isEmpty()) {
            builder.addTextBody("file_url", fileUrl);
        }
        builder.addTextBody("app_id", this.appID);
        builder.addTextBody("conversation_id", conversationId);
        builder.addTextBody("scenario", "assistant");

        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url, builder.build());
        HttpResponse<FileUploadResponse> response =
                httpClient.execute(postRequest, FileUploadResponse.class);

        FileUploadResponse respBody = response.getBody();
        return respBody.getFileId();
    }

    /**
     * 运行AppBuilderClient，根据输入的问题、会话ID、文件ID数组以及是否以流模式返回结果，返回AgentBuilderIterator迭代器。
     *
     * @param query 查询字符串
     * @param conversationId 会话ID
     * @param fileIds 文件ID数组
     * @param stream 是否以流的形式返回结果
     * @return AgentBuilderIterator 迭代器，包含 AgentBuilder 的运行结果
     * @throws IOException 如果在 I/O 操作过程中发生错误
     * @throws AppBuilderServerException 如果 AppBuilder 服务器返回错误
     */
    public AppBuilderClientIterator run(String query, String conversationId, String[] fileIds,
            boolean stream) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.AGENTBUILDER_RUN_URL;
        if (this.appID == null || this.appID.isEmpty()) {
            throw new RuntimeException("Param 'appID' is required!");
        }
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("app_id", this.appID);
        requestBody.put("query", query);
        requestBody.put("conversation_id", conversationId);
        requestBody.put("file_ids", fileIds);
        requestBody.put("stream", stream);
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<StreamIterator<AppBuilderClientResponse>> response =
                httpClient.executeSSE(postRequest, AppBuilderClientResponse.class);
        return new AppBuilderClientIterator(response.getBody());
    }

    /**
     * 执行应用构建客户端运行请求
     *
     * @param requestBody 请求体，包含运行所需的所有信息
     * @return 返回包含构建客户端响应的迭代器
     * @throws IOException 如果在执行请求时发生I/O错误
     * @throws AppBuilderServerException 如果应用构建服务器返回错误响应
     */
    public AppBuilderClientIterator run(AppBuilderClientRunRequest requestBody)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.AGENTBUILDER_RUN_URL;
        if (this.appID == null || this.appID.isEmpty()) {
            throw new RuntimeException("Param 'appID' is required!");
        }

        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<StreamIterator<AppBuilderClientResponse>> response = httpClient.executeSSE(postRequest,
                AppBuilderClientResponse.class);
        return new AppBuilderClientIterator(response.getBody());
    }

    /**
     * 对对话结果进行点踩点赞
     *
     * @param requestBody 请求体，包含运行所需的所有信息
     * @return 返回包含构建客户端响应的迭代器
     * @throws IOException               如果在执行请求时发生I/O错误
     * @throws AppBuilderServerException 如果应用构建服务器返回错误响应
     */
    public AppBuilderClientFeedbackResponse feedback(AppBuilderClientFeedbackRequest requestBody)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.FEEDBACK_URL;

        if (requestBody.getAppId() == null || requestBody.getAppId().isEmpty()) {
            requestBody.setAppId(this.appID);
        }

        if (requestBody.getAppId() == null || requestBody.getAppId().isEmpty()) {
            throw new RuntimeException("Param 'appID' is required!");
        }

        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<AppBuilderClientFeedbackResponse> response = httpClient.execute(postRequest, AppBuilderClientFeedbackResponse.class);
        AppBuilderClientFeedbackResponse respBody = response.getBody();
        return respBody;
    }
}
